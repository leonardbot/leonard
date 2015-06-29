import wikipedia

module_config = {
    "name": "wikipedia",
    "public_name": {
        "en": "Wikipedia",
        "ru": "Википедия"
    },
    "description": {
        "en": "Search page in Wikipedia",
        "ru": "Искать статью в Википедии"
    },
    "regexps": {
            "en": [
                "!wiki(pedia)? (.+)"
            ],
            "ru": [
                "!вики(педия)? (.+)"
            ]
    },
    "command_format": {
        "en": "!wiki <article name>",
        "ru": "!вики <название статьи>"
    },
    "examples": {
        "en": [
            "!wiki cat",
            "!wiki Theory of Big Bang"
        ],
        "ru": [
            "!вики кошка",
            "!вики Теория большого взрыва"
        ]
    },
    "adapters": []
}

page_error_message = {
    'en': "I don't know",
    'ru': "Я не знаю"
}

def get_answer(message, lang, bot, options):
    wikipedia.set_lang(bot.language)
    article_title = options[1]
    summary = ""
    try:
        summary = wikipedia.summary(article_title, sentences=5)
    except wikipedia.exceptions.PageError:
        bot.send_message(
            message_text=page_error_message[bot.language],
            sender_id=message['sender_id'],
            sender_type=message['sender_type']
        )
    except wikipedia.exceptions.DisambiguationError as error:
        # There is a bug in wikipedia module.
        # I fix it with this magic.
        try:
            summary = wikipedia.summary(error.options[0], sentences=5)
        except wikipedia.exceptions.DisambiguationError as error_2:
            try:
                summary = wikipedia.summary(error_2.options[1], sentences=5)
            except wikipedia.exceptions.DisambiguationError:
                return False
    if summary:
        bot.send_message(
            message_text=summary,
            sender_id=message['sender_id'],
            sender_type=message['sender_type']
        )
        return True
    else:
        return False