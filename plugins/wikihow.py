"""
name: wikihow
description: plugin for getting information from wikihow
priority: 100
"""

import json
import requests
import leonard
from leonard.utils import wikimarkup

WIKIHOW_SEARCH_API = ('http://{}wikihow.com/api.php?action=query&list=search'
                      '&srnamespace=0&srprop=titlesnippet%7Csnippet&'
                      'srsearch={}&format=json')
WIKIHOW_ARTICLE = 'http://{}wikihow.com/index.php?title={}&action=raw'


def page_exists(message, bot):
    """
    Check, is in the Wikihow article about user's requests
    Saves article title in message.variables and returns True/False
    """
    url = WIKIHOW_SEARCH_API.format(bot.get_locale(
                                        'wikihow',
                                        message.sender.data['language']
                                    ).language_subdomain,
                                    message.text)
    # Try to get response from cache
    response = bot.storage.get('url["{}"]'.format(url))
    # If we got response from Redis, decode it to string
    if response:
        response = response.decode('utf-8')
    else:
        response = requests.get(url).text
        bot.storage.set('url["{}"]'.format(url), response)
    response = json.loads(response)
    # If there is a results, so save first in variables and return True
    if response['query']['search']:
        message.variables['wikihow_title'] = (
            response['query']['search'][0]['title'].replace(' ', '+')
        )
        return True
    return False


@leonard.hooks.callback(page_exists)
def article_message(message, bot):
    url = WIKIHOW_ARTICLE.format(message.locale.language_subdomain,
                                 message.variables['wikihow_title'])
    article_markup = requests.get(url).text
    messages = wikimarkup.parse_wikihow_markup(article_markup)
    # Send article title
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.variables['wikihow_title'].replace('+', ' ').capitalize()
    )
    bot.send_message(answer)
    for message_text in messages:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message_text,
            variables={"telegram_hide_preview": True}
        )
        bot.send_message(answer)
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.source.format(url.rstrip('&action=raw')),
        variables={"telegram_hide_preview": True}
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'
    language_subdomain = ''
    source = 'Source: {}'


class RussianLocale:
    language_code = 'ru'
    language_subdomain = 'ru.'
    source = 'Источник: {}'
