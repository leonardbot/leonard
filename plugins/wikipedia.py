"""
name: wikipedia
description: get data from Wikipedia.org
priority: 350
"""
import json
import requests

import leonard
from leonard.utils import strip_tags

WIKIPEDIA_SUMMARY_API = ('https://{}.wikipedia.org/w/api.php?'
                         'action=query&list=search&srsearch={}&format=json')
WIKIPEDIA_ARTICLE_URL = 'https://{}.wikipedia.org/wiki/{}'


def get_wiki_summary(query, message):
    url = WIKIPEDIA_SUMMARY_API.format(message.locale.language_code, query)
    response = json.loads(requests.get(url).text)
    if not response['query']['search']:
        return None
    return message.locale.summary.format(
        strip_tags(response['query']['search'][0]['snippet']),
        WIKIPEDIA_ARTICLE_URL.format(message.locale.language_code,
                                     response['query']['search'][0]['title'])
                             .replace(' ', '_')
    )


@leonard.hooks.ross(type='wikipedia', subtype='summary')
def summary_message(message, bot):
    summary = get_wiki_summary(message.variables['ross']['query'], message)
    if not summary:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.dont_know
        )
        bot.send_message(answer)
        return
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=summary
    )
    bot.send_message(answer)


class EnglishLocale(leonard.locale.EnglishLocale):
    language_code = 'en'
    dont_know = "I don't know 😬"
    summary = '{}\n\n{}'


class RussianLocale(leonard.locale.RussianLocale):
    language_code = 'ru'
    dont_know = "Я не знаю 😬"
    summary = '{}\n\n{}'
