module_config = {
    "name": "say",
    "public_name": {
        "en": "Say",
        "ru": "Сказать"
    },
    "description": {
        "en": "Bot will say what are you want",
        "ru": "Заставить бота сказать что-нибудь"
    },
    "regexps": {
            "en": [
                "!say (.+)"
            ],
            "ru": [
                "!скажи (.+)"
            ]
    },
    "command_format": {
        "en": "!say <words>",
        "ru": "!скажи <фраза>"
    },
    "examples": {
        "en": [
            "!say Hello world!",
            "!say I love python"
        ],
        "ru": [
            "!скажи Привет, мир!",
            "!скажи Я люблю питон"
        ]
    },
    "adapters": []
}


def get_answer(message, lang, bot, options):
    bot.send_message(
        message_text=options[0],
        sender_id=message['sender_id'],
        sender_type=message['sender_type']
    )
    return True