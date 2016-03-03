# -*- coding: utf-8 -*-

"""
@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015
"""

import time
import pickle
import threading

import schedule

from leonard import adapter
from leonard import config
from leonard import db
from leonard import exceptions
from leonard import manager
from leonard import storage
from leonard.utils import logger, analytics, NextHook


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
        logger.info_message('Loading config')

        self.config = config.Config(
            prefix=command_line_arguments['config-prefix']
        )

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
        logger.info_message('Connecting to redis storage')
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
        logger.info_message('Connecting to database')
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
        logger.info_message('Loading adapter')

        self.adapter = adapter.load_adapter(command_line_arguments['adapter'])

        # If load adapter function return None, stop the bot.
        if not self.adapter:
            logger.info_message('Quiting')
            exit()

        # Collect config variables from adapter.
        for variable in self.adapter.config.variables:
            if variable not in self.config.variables:
                self.config.variables[variable] = (
                     self.adapter.config.variables[variable]
                )

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

        interval_thread = threading.Thread(
            target=self.start_interval_hooks,
            args=()
        )
        interval_thread.start()

        for message in self.adapter.module.get_messages(self):
            # Parse message in new thread
            message_thread = threading.Thread(
                target=self.parse_message,
                args=(message, )
            )
            message_thread.start()

    def parse_message(self, message):
        """
        Prepare message, check for all hooks of plugins and call matched hook

        :param message: IncomingMessage object
        :return:
        """
        logger.info_message('Got message', message)

        # Connect users middleware
        message.sender = self.database.find_by_adapter_id(message.adapter_id)
        # If we know message.sender language, add it to message.language
        if 'language' in message.sender.data:
            message.language = message.sender.data['language']
        else:
            logger.warning_message('Language not set for ', message)

        # If some adapter's variables not saved in DB or changed,
        # update it
        for variable in message.variables:
            if (variable not in message.sender.data or
                    message.variables[variable] != message.sender.data[variable]):
                message.sender.data[variable] = message.variables[variable]
        message.sender.update()

        if ('question' in message.sender.data and
                message.sender.data['question'] != ''):
            logger.info_message('Detected question answer for', message)
            # Parse question callback
            callback = pickle.loads(message.sender.data['question'])
            # Delete question, but save plugin name
            plugin_name = message.sender.data['question_plugin']
            message.sender.data['question'] = ''
            message.sender.update()
            # Add correct locale for message
            user_locale = message.sender.data.get('language', None)
            if user_locale:
                plugin = self.plugins_manager.get_plugin_by_name(plugin_name)
                message.locale = plugin.localization.get(user_locale)
            # Run callback
            callback(message, self)
            return

        found_hooks = []
        for plugin in self.plugins_manager.plugins:
            hooks = plugin.check_hooks(message)
            found_hooks.extend(hooks)

        if not found_hooks:
            logger.warning_message('Hooks not found for', message)
            return
        logger.info_message('Found', len(found_hooks), 'hooks')
        # Sort found hooks by priority of plugin and priority of hook,
        # than call the most appropriate
        found_hooks.sort(
            key=lambda h: (
                h.plugin.config.priority,
                h.priority
            ),
            reverse=True
        )

        for hook in found_hooks:
            # Add correct locale for message
            user_locale = message.sender.data.get('language', None)
            if user_locale:
                message.locale = hook.plugin.localization.get(user_locale)

            try:
                hook.call(message, self)
            except NextHook:
                continue

            # Track message using Botan.io analytics in new thread
            analytics_thread = threading.Thread(
                target=analytics.track_message,
                kwargs={
                    'message': message.variables['last_message'],
                    'adapter': self.adapter.name,
                    'plugin': hook.plugin.name,
                    'bot': self
                }
            )
            analytics_thread.start()
            return

    def start_interval_hooks(self):
        """
        Start all interval hooks in plugins using schedule module

        :return:
        """
        for plugin in self.plugins_manager.plugins:
            for hook in plugin.interval_hooks:
                # Call hook with bot argument
                hook.interval.do(lambda: hook.call(self))
                logger.info_message('Added interval hook', hook)

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
        logger.info_message('Sending message', message)
        self.adapter.module.send_message(message, self)

    @exceptions.catch_module_errors
    def ask_question(self, message, callback, plugin_name):
        """
        Ask about something the user from plugin.

        :param message: OutgoingMessage object
        :param callback: function that called with (message, bot)
                         after users next message
        :param plugin_name: str, name of plugin that asks question
        :return:
        """
        logger.info_message('Asking question', message)
        message.is_question = True
        self.send_message(message)
        message.recipient.data['question'] = pickle.dumps(callback)
        message.recipient.data['question_plugin'] = plugin_name
        message.recipient.update()

    def get_locale(self, plugin_name, language_code):
        """
        Get plugin locale from bot object. It's needed in interval hooks.

        :param plugin_name: str, plugin name
        :param language_code: str, two-letters locale language code
        :return: locale class, like EnglishLocale
        """
        # Convert short plugin name to full name.
        # For example, 'hello' => 'plugins.hello'
        plugin_name = 'plugins.' + plugin_name

        for plugin in self.plugins_manager.plugins:
            if plugin_name == plugin.name:
                return plugin.localization.get(language_code)
        logger.error_message("Didn't find '{}' locale for {} plugin".format(
            language_code, plugin_name
        ))
