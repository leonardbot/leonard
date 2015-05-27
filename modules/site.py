import requests

module_config = {
    "name": "site",
    "public_name": {
        "en": "Site",
        "ru": "Сайт"
    },
    "description": {
        "en": "Is site working?",
        "ru": "Проверить, работает ли сайт"
    },
    "regexps": {
            "en": [
                "!site (.+)"
            ],
            "ru": [
                "!сайт (.+)"
            ]
    },
    "command_format": {
        "en": "!site <site url>",
        "ru": "!сайт <адрес сайта>"
    },
    "examples": {
        "en": [
            "!site facebook.com",
            "!site http://yandex.ru"
        ],
        "ru": [
            "!сайт ya.ru",
            "!сайт https://google.com"
        ]
    },
    "adapters": []
}

site_working_message = {
    'en': 'Site working',
    'ru': 'Сайт работает'
}

site_not_working_message = {
    'en': 'Site not working',
    'ru': 'Сайт не работает'
}

def get_answer(message, lang, bot, options):
    if 'https://' not in options[0] and 'http://' not in options[0]:
        site_url = 'http://' + options[0]
    else:
        site_url = options[0]
    try:
        response = requests.get(site_url)
    except requests.exceptions.ConnectionError:
        answer = site_not_working_message[bot.language]
    else:
        if response.status_code == 200:
            answer = site_working_message[bot.language]
        else:
            answer = site_not_working_message[bot.language]

    bot.send_message(
        message_text=answer,
        sender_id=message['sender_id'],
        sender_type=message['sender_type']
    )
    return True