# -*- coding: utf-8 -*-

"""
Functions and ready messages for plugin localization

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015-2016
"""

ENGLISH_EXPORT = {
    'question_explanation': ("You can answer question in 1 hour - "
                             "or I will forget about it.\n"
                             "If you don't want to answer - just send 'Oops' "
                             "and consider it gone.")
}

RUSSIAN_EXPORT = {
    'question_explanation': ('Ты можешь ответить на вопрос в течение часа,'
                             'потому что потом я могу забыть о нем.\n'
                             'Если не хочешь отвечать, отправь "Ой" и '
                             'будем считать, что ничего не было.')
}

LANGUAGE_EXPORTS = {
    'en': ENGLISH_EXPORT,
    'ru': RUSSIAN_EXPORT
}

def get(language_code):
    """
    Get a dict with some phrases and functions for generating them.

    :param language_code: str, language for phrases
    :return: dict with phrases and functions
    """
    return LANGUAGE_EXPORTS[language_code]
