# -*- coding: utf-8 -*-

"""
Manager for locales: finding locals in plugins,
adding correct local for user

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015
"""

from leonard.utils import logger


def find_locales(plugin):
    """
    Find locale classes in plugin module and return list of objects

    :param plugin: Plugin object
    :return: PluginLocalization object
    """
    locales = []
    for (object_name, plugin_object) in plugin.module.__dict__.items():
        if object_name.endswith('Locale'):
            locale = PluginLocale(plugin_object)
            locales.append(locale)
    return PluginLocalization(plugin, locales)

class PluginLocalization:
    """
    Class for storing plugin locales
    """
    def __init__(self, plugin, locales):
        """
        Create plugin localization with all locales

        :param plugin: Plugin object
        :param locales: list of PluginLocale object
        :return:
        """
        self.plugin = plugin
        self.locales = locales

    def get(self, language_code):
        """
        Get plugin locale with correct language_code

        :param language_code: two-letters language code, like 'en'
        :return: class of locale, like EnglishLocale of hello plugin
        """
        for locale in self.locales:
            if locale.language_code == language_code:
                return locale.locale_class()

        logger.error_message(
            "Din't found locale with", language_code, 'in', str(self.plugin)
        )
        return None


class PluginLocale:
    """
    Class for storing language locale for plugin
    """
    def __init__(self, locale_class):
        """
        Create new language locale

        :param locale_class: class of locale, like EnglishLocale of hello plugin
        """
        self.language_code = locale_class().language_code
        self.locale_class = locale_class


class EnglishLocale:
    default = 'default'
    more = 'More'
    question_explanation = ("You can answer question in 1 hour - "
                            "or I will forget about it.\n"
                            "If you don't want to answer - just send 'Oops' "
                            "and consider it gone.")


class RussianLocale:
    default = 'Обычное'
    more = 'Больше'
    question_explanation =  ('Ты можешь ответить на вопрос в течение часа, '
                             'потому что потом я могу забыть о нем.\n'
                             'Если не хочешь отвечать, отправь "Ой" и '
                             'будем считать, что ничего не было.')
