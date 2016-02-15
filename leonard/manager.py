# -*- coding: utf-8 -*-

"""
Manager for plugins: importing and loading

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015
"""

import threading
import importlib

from leonard.utils import logger
from leonard.hooks import find_hooks
from leonard.locale import find_locales
from leonard.config import parse_config
from leonard.exceptions import catch_module_errors


class PluginsManager:
    def __init__(self, config):
        """
        Create plugins manager

        :param config: Config object with bot information
        :return:
        """
        self.config = config
        self.plugins = []

    def load_plugins(self):
        """
        Load plugins from 'installed_plugins.txt' file

        :return: list of Plugin objects
        """
        plugin_names = self.config.installed_plugins
        for plugin_name in plugin_names:
            self.load_plugin(plugin_name)

    def reload_plugins(self):
        """
        Reload all imported and loaded plugins

        :return:
        """
        for plugin in self.plugins:
            plugin.reload_plugin()

    def load_plugin(self, plugin_name):
        """
        Parse config, find hooks and create new Plugin object.

        :param plugin_name: name for plugin import
        :return:
        """
        plugin_name = plugin_name.strip()
        plugin_module = import_plugin(plugin_name)
        if not plugin_module:
            logger.error_message("'{}' plugin didn't load".format(
                plugin_name
            ))
            return
        plugin_config = parse_config(plugin_module, 'plugin')
        # Create new Plugin object with no hooks and no interval hooks
        plugin = Plugin(plugin_name, plugin_module, plugin_config,
                        [], [])
        # Set plugin hooks and interval hooks by find_hooks function
        plugin.hooks, plugin.interval_hooks = find_hooks(plugin)
        plugin.localization = find_locales(plugin)
        self.plugins.append(plugin)

    def get_plugin_by_name(self, plugin_name):
        """
        Get plugin by its name

        :param plugin_name: str, short plugin name, like 'weather'
        :return: Plugin object
        """
        # Convert plugin_name to full plugin name
        plugin_name = 'plugins.' + plugin_name
        for plugin in self.plugins:
            if plugin.name == plugin_name:
                return plugin
        return None


class Plugin:
    def __init__(self, name, module, config, hooks, interval_hooks):
        """
        Create new plugin

        :param name: string, module name
        :param module: module, imported plugin module
        :param config: ModuleConfig object, parsed plugin config
        :param hooks: list of Hook objects
        :param interval_hooks: list of IntervalHooks objects
        :return:
        """
        self.name = name
        self.module = module
        self.config = config
        self.hooks = hooks
        self.interval_hooks = interval_hooks
        self.localization = None

    def __str__(self):
        return 'Plugin <' + self.name + '>'

    def reload_plugin(self):
        """
        Reload plugin (import it and find hooks again)

        :return:
        """
        self.module = importlib.reload(self.module)
        self.config = parse_config(self.module, 'plugin')
        self.hooks = find_hooks(self)

    def check_hooks(self, message):
        """
        Check incoming message for plugin's hooks

        :param message: IncomingMessage object
        :return: Hook object or None
        """
        threads = []
        # Save found hooks in one object for all threads
        found_hooks = FoundHooks()
        for hook in self.hooks:
            thread = threading.Thread(target=check_hook,
                                      args=(hook, message, found_hooks))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        # Convert FoundHooks object to list with hooks
        found_hooks = found_hooks.data

        if found_hooks:
            found_hooks.sort(key=lambda h: h.priority, reverse=True)
            return found_hooks[0]
        else:
            return None


class FoundHooks:
    """
    Already found hooks while processing message.
    It's important because we checking hooks in threads.
    """
    def __init__(self):
        """
        Create object for saving found hooks
        """
        self.data = []


def check_hook(hook, message, found_hooks):
    """
    Check hook and if it matched add it to found hooks

    :param hook: Hook object
    :param message: IncomingMessage object
    :param found_hooks: FoundHooks object
    :return:
    """
    if hook.check(message):
        found_hooks.data.append(hook)


def import_plugin(plugin_name):
    """
    Import plugin using importlib

    :param plugin_name: full name of plugin, ex. 'plugins.console'
    :return: module object or None if plugin not found
    """
    try:
        return importlib.import_module(plugin_name)
    except Exception as error:
        logger.error_message('Error with loading {}: \n {}'.format(
            plugin_name, str(error)
        ))
        return None
