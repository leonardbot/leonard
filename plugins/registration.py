"""
name: registration
description: "Module that catching users who using bot first time"
priority: 1000
"""
import leonard


language_variants = (
    '1) English - enter "en" or "1"',
    '2) Русский - введите "ru" или "2"'
)

languages_dict = {
     'en': ['en', 'english', '1'],
     'ru': ['ru', 'russian', 'русский', '2']
}

before_registration = (
    'Choose language: / Выберите язык:\n' +
    '\n'.join(language_variants)
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
        text=before_registration,
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
    # Normalize message
    message_text = message.text.lower().rstrip().lstrip()
    language = None
    for (language_code, variants) in languages_dict.items():
        for variant in variants:
            if message_text == variant:
                language = language_code
                break

    if language is None:
        question = leonard.OutgoingMessage(
            text=before_registration,
            recipient=message.sender
        )
        bot.ask_question(question, registration_callback)
        return

    message.sender.data['language'] = language
    message.sender.update()
    answer = leonard.OutgoingMessage(
        text=bot.get_locale('registration', language).success_register,
        recipient=message.sender
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'
    success_register = 'Hi! I want to be your friend :) Do you want something?'


class RussianLocale:
    language_code = 'ru'
    success_register = (
        'Привет! Я рад, что мы теперь друзья :) '
        'Тебе нужно что-нибудь?'
    )
