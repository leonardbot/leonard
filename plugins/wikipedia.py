"""
name: wikipedia
description: get data from Wikipedia.org
priority: 300
"""

import requests
import leonard


def get_wiki_summary(query, message):
    return 'lulz'


@leonard.hooks.ross(type='wikipedia', subtype='summary')
def summary_message(message, bot):
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=get_wiki_summary(message.variables['ross']['query'], message)
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'


class RussianLocale:
    language_code = 'ru'
