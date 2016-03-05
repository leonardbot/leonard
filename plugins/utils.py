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
    question_explanation = ("You can answer question in 1 hour - "
                            "or I will forget about it.\n"
                            "If you don't want to answer - just send 'Oops' "
                            "and consider it gone.")


class RussianLocale:
    language_code = 'ru'
    cancel_from_question = 'Ладно.'
    question_explanation =  ('Ты можешь ответить на вопрос в течение часа,'
                             'потому что потом я могу забыть о нем.\n'
                             'Если не хочешь отвечать, отправь "Ой" и '
                             'будем считать, что ничего не было.')
