import json
import requests
from utils.download_photo import download_photo

module_config = {
    "name": "butts",
    "public_name": {
        "en": "Butts",
        "ru": "Попа"
    },
    "description": {
        "en": "No comments",
        "ru": "Без комментариев"
    },
    "regexps": {
            "en": [
                "!butts"
            ],
            "ru": [
                "!попа"
            ]
    },
    "command_format": {
        "en": "!butts",
        "ru": "!попа"
    },
    "examples": {
        "en": [
            "!butts"
        ],
        "ru": [
            "!попа"
        ]
    },
    "adapters": []
}


def get_answer(message, lang, bot, options):
    response = requests.get('http://api.obutts.ru/noise/1')
    butts_url = 'http://media.obutts.ru/' + json.loads(
        response.text
    )[0]['preview']

    bot.send_message(
        message_photos=[download_photo(butts_url)],
        sender_id=message['sender_id'],
        sender_type=message['sender_type']
    )
    return True