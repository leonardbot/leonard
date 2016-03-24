"""
name: uber
description: get taxi from Uber
priority: 300
"""

import leonard


@leonard.hooks.ross(type='taxi', subtype='get')
def get_taxi_message(message, bot):
    pass


class EnglishLocale(leonard.locale.EnglishLocale):
    language_code = 'en'

    choose_location = 'Not a problem, I can get taxi for you.'


class RussianLocale(leonard.locale.RussianLocale):
    language_code = 'ru'
