import json
import requests
from utils.download_photo import download_photo

module_config = {
    "name": "boobs",
    "public_name": {
        "en": "Boobs",
        "ru": "Сиськи"
    },
    "description": {
        "en": "No comments",
        "ru": "Без комментариев"
    },
    "regexps": {
            "en": [
                "!boobs"
            ],
            "ru": [
                "!сиськи"
            ]
    },
    "command_format": {
        "en": "!boobs",
        "ru": "!сиськи"
    },
    "examples": {
        "en": [
            "!boobs"
        ],
        "ru": [
            "!сиськи"
        ]
    },
    "adapters": []
}


def get_answer(message, lang, bot, options):
    response = requests.get('http://api.oboobs.ru/noise/1')
    butts_url = 'http://media.oboobs.ru/' + json.loads(
        response.text
    )[0]['preview']

    bot.send_message(
        message_photos=[download_photo(butts_url)],
        sender_id=message['sender_id'],
        sender_type=message['sender_type']
    )
    return True