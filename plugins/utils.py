"""
name: utils
description: reusable bot messages, like cancel from question
priority: 100
"""

import leonard


def cancel_from_question(message, bot):
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=bot.get_locale(
            'utils', message.sender.data.get('language', 'en')
        ).cancel_from_question
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'
    cancel_from_question = 'Fine.'


class RussianLocale:
    language_code = 'ru'
    cancel_from_question = 'Ладно.'
