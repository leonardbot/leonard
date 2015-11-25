# -*- coding: utf-8 -*-

"""
@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""

import time
import _thread as thread
import schedule

from sheldon import adapter
from sheldon import config
from sheldon import exceptions
from sheldon import manager
from sheldon import storage
from sheldon.utils import logger


class Sheldon:
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

        self._load_storage()

        self._load_adapter(command_line_arguments)

        self._load_plugins()

    def _load_config(self, command_line_arguments):
        """
        Create and load bot config.

        :param command_line_arguments: dict, arguments for creating config:
                                       config-prefix - prefix of environment
                                                       variables.
                                                       Default - 'SHELDON_'
        :return:
        """
        self.config = config.Config(prefix=command_line_arguments['config-prefix'])

        # If we had problems with config loading, stop the bot.
        if not self.config:
            logger.info_message('Quiting')
            exit()

    def _load_storage(self):
        """
        Connect to bot storage in Redis

        :return:
        """
        self.storage = storage.Storage(self)

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
        thread.start_new_thread(self.start_interval_hooks, ())

        for message in self.adapter.module.get_messages(self):
            hook = self.parse_message(message)
            if hook:
                hook.call(message, self)

    def parse_message(self, message):
        """
        Check message for all hooks of plugins

        :param message: IncomingMessage object
        :return: Hook object or None
        """
        found_hooks = []
        for plugin in self.plugins_manager.plugins:
            hook = plugin.check_hooks(message)
            if hook is not None:
                found_hooks.append(hook)

        if found_hooks:
            found_hooks.sort(key=lambda h: h.priority, reverse=True)
            return found_hooks[0]
        else:
            return None

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
