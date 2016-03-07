"""
name: registration
description: "Module that catching users who using bot first time"
priority: 1000
"""
import leonard


LANGUAGE_VARIANTS = (
    '1) English - enter "en" or "1"',
    '2) Русский - введите "ru" или "2"'
)

LANGUAGE_BUTTONS = [
     ['English'],
     ['Русский']
]

LANGUAGES_DICT = {
     'en': ['en', 'english', '1'],
     'ru': ['ru', 'russian', 'русский', '2']
}

BEFORE_REGISTRATION = (
    'Choose language: / Выберите язык:\n' +
    '\n'.join(LANGUAGE_VARIANTS)
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
        text=BEFORE_REGISTRATION,
        recipient=message.sender,
        buttons=LANGUAGE_BUTTONS
    )
    bot.ask_question(question, language_callback, 'registration')


def language_callback(message, bot):
    """
    Function calling when user choosing language

    :param message:
    :param bot:
    :return:
    """
    # Normalize message
    message_text = message.text.lower().rstrip().lstrip()
    language = None
    for (language_code, variants) in LANGUAGES_DICT.items():
        for variant in variants:
            if message_text == variant:
                language = language_code
                break

    if language is None:
        question = leonard.OutgoingMessage(
            text=BEFORE_REGISTRATION,
            recipient=message.sender,
            buttons=LANGUAGE_BUTTONS
        )
        bot.ask_question(question, language_callback, 'registration')
        return

    message.sender.data['language'] = language
    message.sender.update()
    # Ask about location
    answer = leonard.OutgoingMessage(
        text=bot.get_locale('registration', language).send_location,
        recipient=message.sender
    )
    bot.ask_question(answer, location_callback, 'registration')


def location_callback(message, bot):
    if not message.location:
        answer = leonard.OutgoingMessage(
            text=message.locale.send_location,
            recipient=message.sender
        )
        bot.ask_question(answer, location_callback, 'registration')
        return
    message.sender.update_location_data(message.location)
    answer = leonard.OutgoingMessage(
        text=message.locale.success_register,
        recipient=message.sender
    )
    bot.send_message(answer)



class EnglishLocale:
    language_code = 'en'
    send_location = (
        'Your location is needed by many plugins, like news or weather. '
        'Please send me your location (not real, if real location is secret)'
    )
    success_register = 'Hi! I want to be your friend :) BOT FUNCTIONS HERE'


class RussianLocale:
    language_code = 'ru'
    send_location = (
         'Ваше местоположение нужно для многих функций бота, как новости или '
         'погода. Пожалуйста, отправьте ваше местоположение (можно не настоящее'
         ', если хотите сохранить его в секрете)'
    )
    success_register = (
        'Привет! Я рад, что мы теперь друзья :) '
        'Здесь будет описание различных возможностей бота, инструкция как '
        'перерегистрироваться'
    )
