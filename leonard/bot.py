# -*- coding: utf-8 -*-

"""
@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""

import time
import pickle
import _thread as thread

import schedule

from leonard import adapter
from leonard import config
from leonard import db
from leonard import exceptions
from leonard import manager
from leonard import storage
from leonard.utils import logger, analytics


class Leonard:
    """
    Main class of the bot.
    Run script creating new instance of this class and run it.
    """

    def __init__(self, command_line_arguments):
        """
        Function for loading bot.

        :param command_line_arguments: dict, arguments for start script
        :return:
        """

        self._load_config(command_line_arguments)

        self._load_storage(command_line_arguments)

        self._load_database(command_line_arguments)

        self._load_adapter(command_line_arguments)

        self._load_plugins()

    def _load_config(self, command_line_arguments):
        """
        Create and load bot config.

        :param command_line_arguments: dict, arguments for creating config:
                                       config-prefix - prefix of environment
                                                       variables.
                                                       Default - 'LEONARD_'
        :return:
        """
        self.config = config.Config(prefix=command_line_arguments['config-prefix'])

        # If we had problems with config loading, stop the bot.
        if not self.config:
            logger.info_message('Quiting')
            exit()

    def _load_storage(self, command_line_arguments):
        """
        Connect to bot storage in Redis

        :param command_line_arguments: dict, arguments for creating config:
                                       config-prefix - prefix of environment
                                                       variables.
                                                       Default - 'LEONARD_'
        :return:
        """
        self.storage = storage.Storage(
            self, command_line_arguments['config-prefix']
        )

    def _load_database(self, command_line_arguments):
        """
        Connect to bot db in MongoDB

        :param command_line_arguments: dict, arguments for creating config:
                                       config-prefix - prefix of environment
                                                       variables.
                                                       Default - 'LEONARD_'
        :return:
        """
        self.database = db.Database(
            self, command_line_arguments['config-prefix']
        )

    def _load_adapter(self, command_line_arguments):
        """
        Load adapter.

        :param command_line_arguments: dict, arguments for creating config:
                                       adapter - name of adapter.
                                                 May be local package in
                                                 adapters folder or package
                                                 from PyPi.
                                                 Default - 'console'.
        :return:
        """
        self.adapter = adapter.load_adapter(command_line_arguments['adapter'])

        # If load adapter function return None, stop the bot.
        if not self.adapter:
            logger.info_message('Quiting')
            exit()

        # Collect config variables from adapter.
        for variable in self.adapter.config.variables:
            if variable not in self.config.variables:
                self.config.variables[variable] = self.adapter.config.variables[variable]

    def _load_plugins(self):
        """
        Load plugins from plugins folder or PyPi using plugins manager.
        
        :return:
        """
        self.plugins_manager = manager.PluginsManager(self.config)

        # Run function for searching and importing new plugins
        self.plugins_manager.load_plugins()

        # Collect config variables from plugins.
        for plugin in self.plugins_manager.plugins:
            # If plugin defined a variable with default value
            # and user didn't set this variable,
            # set variable to default value.
            for variable in plugin.config.variables:
                if variable not in self.config.variables:
                    self.config.variables[variable] = plugin.config.variables[variable]

    def start(self):
        """
        Start getting, parsing and answering messages

        :return:
        """
        logger.info_message('Starting bot')

        thread.start_new_thread(self.start_interval_hooks, ())

        for message in self.adapter.module.get_messages(self):
            # Parse message in new thread
            thread.start_new_thread(self.parse_message, (message, ))

    def parse_message(self, message):
        """
        Prepare message, check for all hooks of plugins and call matched hook

        :param message: IncomingMessage object
        :return:
        """
        # Connect users middleware
        message.sender = self.database.find_by_adapter_id(message.adapter_id)
        if 'language' in message.sender.data:
            message.language = message.sender.data['language']
        else:
            logger.warning_message(
                'Language not set for {} user'.format(message.adapter_id)
            )
            message.language = self.config.get(
                'LEONARD_DEFAULT_LANGUAGE', 'en'
            )

        # If some adapter's variables not saved in DB or changed,
        # update it
        for variable in message.variables:
            if (variable not in message.sender.data or
                  message.variables[variable] != message.sender.data[variable]):
                message.sender.data[variable] = message.variables[variable]
                message.sender.update()

        if ('question' in message.sender.data and
                message.sender.data['question'] != ''):
            # Parse question callback
            callback = pickle.loads(message.sender.data['question'])
            # Delete question
            message.sender.data['question'] = ''
            message.sender.update()
            # Run callback
            thread.start_new_thread(callback, (message, self))
            return

        found_hooks = []
        for plugin in self.plugins_manager.plugins:
            hook = plugin.check_hooks(message)
            if hook is not None:
                found_hooks.append(hook)

        if found_hooks:
            # Sort found hooks by priority of plugin and priority of hook,
            # than call the most appropriate
            found_hooks.sort(
                key=lambda h: (
                    h.plugin.config.priority,
                    h.priority
                ),
                reverse=True
            )
            thread.start_new_thread(analytics.track_message, (), {
                'message': message.variables['last_message'],
                'adapter': self.adapter.name,
                'plugin': found_hooks[0].plugin.name,
                'bot': self
            })
            found_hooks[0].call(message, self)

    def start_interval_hooks(self):
        """
        Start all interval hooks in plugins using schedule module

        :return:
        """
        for plugin in self.plugins_manager.plugins:
            for hook in plugin.interval_hooks:
                # Call hook with bot argument
                hook.interval.do(lambda: hook.call(self))

        while True:
            schedule.run_pending()
            time.sleep(1)

    @exceptions.catch_module_errors
    def send_message(self, message):
        """
        Send outgoing message from plugin

        :param message: OutgoingMessage object
        :return:
        """
        self.adapter.module.send_message(message, self)

    def ask_question(self, message, callback):
        """
        Ask about something the user from plugin.

        :param message: OutgoingMessage object
        :param callback: function that called with (message, bot)
                         after users next message
        :return:
        """
        self.send_message(message)
        message.recipient.data['question'] = pickle.dumps(callback)
        message.recipient.update()
