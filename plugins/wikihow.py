"""
name: wikihow
description: plugin for getting information from wikihow
priority: 100
"""

import time
import json
import requests
import leonard
from leonard.utils import wikimarkup, normalize_message, clean_message

WIKIHOW_SEARCH_API = ('http://{}wikihow.com/api.php?action=query&list=search'
                      '&srnamespace=0&srprop=titlesnippet%7Csnippet&'
                      'srsearch={}&format=json')
WIKIHOW_ARTICLE = 'http://{}wikihow.com/index.php?title={}&action=raw'


def page_exists(message, bot):
    """
    Check, is in the Wikihow article about user's requests
    Saves article title in message.variables and returns True/False
    """
    if 'language' not in message.sender.data:
        return False
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
    # If there is no result, return False
    if 'search' not in response['query'] or not response['query']['search']:
        return False
    # If there is no intersection between title words and user's query words,
    # so return False.
    # Otherwise return True and save Wikihow title
    title = response['query']['search'][0]['title']
    title_words = normalize_message(clean_message(title)).split()
    message_words = message.text.split()
    if not set(title_words).intersection(set(message_words)):
        return False
    message.variables['wikihow_title'] = (
        title.replace(' ', '+')
    )
    return True


@leonard.hooks.callback(page_exists)
def article_message(message, bot):
    url = WIKIHOW_ARTICLE.format(message.locale.language_subdomain,
                                 message.variables['wikihow_title'])
    article_markup = requests.get(url).text
    messages = wikimarkup.parse_wikihow_markup(article_markup)
    # Send article title
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text='{}?'.format(
            message.variables['wikihow_title'].replace('+', ' ').capitalize()
        )
    )
    bot.send_message(answer)
    for message_text in messages:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message_text,
            variables={"telegram_hide_preview": True}
        )
        bot.send_message(answer)
        time.sleep(0.3)
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.source.format(url.rstrip('&action=raw')),
        variables={"telegram_hide_preview": True}
    )
    bot.send_message(answer)


class EnglishLocale(leonard.locale.EnglishLocale):
    language_code = 'en'
    language_subdomain = ''
    source = 'Source: {}'


class RussianLocale(leonard.locale.RussianLocale):
    language_code = 'ru'
    language_subdomain = 'ru.'
    source = 'Источник: {}'
