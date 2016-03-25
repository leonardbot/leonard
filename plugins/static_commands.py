"""
name: static_commands
description: static responses for user's phrases
priority: 350
"""

import random
import leonard
from leonard.utils import keywords_from_words


@leonard.hooks.keywords(
    keywords_from_words(['hello', 'hi', 'привет', 'здраствуй', 'хай'])
)
def hello_message(message, bot):
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=random.choice(message.locale.hello)
    )
    bot.send_message(answer)


class EnglishLocale(leonard.locale.EnglishLocale):
    language_code = 'en'
    hello = ['Hello!', 'Hi!']


class RussianLocale(leonard.locale.RussianLocale):
    language_code = 'ru'
    hello = ['Привет!', 'Здравствуй!']
