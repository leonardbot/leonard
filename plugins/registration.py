"""
name: registration
description: "Module that catching users who using bot first time"
priority: 1000
"""
import leonard

LANGUAGES_LIST = (
    ('English', 'enter', 'en', 'en'),
    ('Русский', 'введите', 'ру', 'ru')
)

question_text = (
    leonard.get_text('registration.choose_language') + '\n' +
    '\n'.join(leonard.get_text('registration.language_variants'))
)


@leonard.hooks.callback(
    lambda message: 'language' not in message.sender.data
)
def registration(message, bot):
    """
    Function run when user first time sending message to bot
    or didn't set language email

    :param message:
    :param bot:
    :return:
    """
    question = leonard.OutgoingMessage(
        text=question_text,
        recipient=message.sender
    )
    bot.ask_question(question, registration_callback)


def registration_callback(message, bot):
    """
    Function calling when user choosing language

    :param message:
    :param bot:
    :return:
    """
    languages_dict = leonard.get_text('registration.languages_dict')
    try:
        language = languages_dict[message.text.lower().rstrip()]
    except KeyError:
        question = leonard.OutgoingMessage(
            text=question_text,
            recipient=message.sender
        )
        bot.ask_question(question, registration_callback)
        return
    message.sender.data['language'] = language
    message.sender.update()
    answer = leonard.OutgoingMessage(
        text=leonard.get_text('registration.introduction', message.sender),
        recipient=message.sender
    )
    bot.send_message(answer)
