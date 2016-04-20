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
    lambda message, bot: 'language' not in message.sender.data
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



class EnglishLocale(leonard.locale.EnglishLocale):
    language_code = 'en'
    send_location = (
        'Your location is needed by many plugins, like news or weather. '
        'Please send me your location (not real, if real location is secret)'
    )
    success_register = (
        """Hi! My name is Leonard and I'm a bot.
It is possible and necessary to chat with me with the human speech because natural communication is the most valuable think we have.
I'm improving all the time and you can write your feedback to seva@leonardbot.xyz and sk@leonardbot.xyz
I can search in the Wikipedia, Wikihow, get taxi (using Uber), tell you weather, news and many different things.
You can read more about me in https://medium.com/@sevazhidkov/leonard-bot-open-source-virtual-assistant-in-messengers-by-russian-school-students-e2b5d1aac9a5#.e2xdsduq5
        """
    )


class RussianLocale(leonard.locale.RussianLocale):
    language_code = 'ru'
    send_location = (
         'Ваше местоположение нужно для многих функций бота, как новости или '
         'погода. Пожалуйста, отправьте ваше местоположение (можно не настоящее'
         ', если хотите сохранить его в секрете)'
    )
    success_register = (
        """Привет, меня зовут Леонард, и, как ни странно, я – бот.
Со мной можно и нужно общаться на человеческом языке, ведь живое общение – самое ценное, что есть у нас. Я постоянно совершенствуюсь, поэтому свои предложения и замечания следует писать seva@leonardbot.xyz и sk@leonardbot.xyz
Я могу: искать в интернете, давать подсказки на все случаи жизни, вызывать такси (если вам повезло жить в зоне действия Uber), узнавать погоду, последние новости и много что ещё.
Подробнее обо мне можно узнать на https://medium.com/@sevazhidkov/leonard-bot-open-source-virtual-assistant-in-messengers-by-russian-school-students-e2b5d1aac9a5#.e2xdsduq5
        """
    )
