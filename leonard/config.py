# -*- coding: utf-8 -*-

"""
@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""

import os
import yaml

from leonard.utils import logger


class Config:
    def __init__(self, prefix='LEONARD_'):
        """
        Load config from environment variables.

        :param prefix: string, all needed environment variables
                            starts from it.
                            Default - 'LEONARD_'. So, environment
                            variables will be looking like:
                            'LEONARD_BOT_NAME', 'LEONARD_TWITTER_KEY'
        :return:
        """
        # Bot config variables
        self.variables = {}

        for variable in os.environ:
            if variable.startswith(prefix):
                self.variables[variable] = os.environ[variable]

        self._set_installed_plugins()

    def get(self, variable, default_value=None):
        """
        Get variable value from environment

        :param variable: string, needed variable
        :param default_value: string, value that returns if
                              variable is not set
        :return: variable value
        """
        if variable not in self.variables:
            return default_value

        return self.variables[variable]

    def _set_installed_plugins(self):
        """
        Create list of installed plugins from installed_plugins.txt
        :return:
        """
        plugins_file = open('installed_plugins.txt')
        self.installed_plugins = plugins_file.readlines()


class ModuleConfig:
    """
    Config class for adapters and basic class for plugins
    """
    def __init__(self, data):
        """
        Create config object for plugin or adapter

        :param data: dict, result of yaml.load()
        :return:
        """
        self.name = data['name']
        self.description = data['description']
        if 'config' in data:
            self.variables = data['config']
        else:
            self.variables = {}
        self._data = data


class PluginConfig(ModuleConfig):
    """
    Config class for plugins
    """
    def __init__(self, data):
        """
        Create new object for plugin config

        :param data: dict, result of yaml.load()
        :return:
        """
        super().__init__(data)
        self.priority = data['priority']


def parse_config(module, type):
    """
    Parse module (plugin/adapter) config in __doc__

    :param module: module object
    :param type: str 'adapter'/'plugin'
    :return: ModuleConfig object
    """
    if not hasattr(module, '__doc__'):
        logger.error_message('__doc__ config not found in {}'.format(module))
        return None

    config_text = module.__doc__
    try:
        config_data = yaml.load(config_text)
    except yaml.scanner.ScannerError as error:
        logger.error_message('Error while reading {} config \n {}'.format(
            module,
            error.__traceback__
        ))
        return None

    if type == 'plugin':
        config = PluginConfig(config_data)
    else:
        config = ModuleConfig(config_data)
    return config




