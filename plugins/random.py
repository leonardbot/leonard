"""
name: news
description: "Get last news from Google News or Yandex News"
priority: 250
"""

import random

import leonard
import leonard.utils

RANDOM_WORDS = ['рандом', 'ранд', 'случайное', 'рандомное',
                'число', 'random', 'number', 'rand']


@leonard.hooks.keywords(leonard.utils.keywords_from_words(RANDOM_WORDS))
def random_number_message(message, bot):
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.your_random.format(random.randint(1, 1000))
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'
    your_random = 'Your random number is {}'


class RussianLocale:
    language_code = 'ru'
    your_random = 'Твое рандомное число - '
