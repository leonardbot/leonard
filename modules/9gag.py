import json
import requests
import random
from utils.download_photo import download_photo

module_config = {
    "name": "9gag",
    "public_name": {
        "en": "9GAG",
        "ru": "9GAG"
    },
    "description": {
        "en": "Show random post from 9GAG",
        "ru": "Показать случайный пост из 9GAG"
    },
    "regexps": {
            "en": [
                "!9gag"
            ],
            "ru": [
                "!9gag"
            ]
    },
    "command_format": {
        "en": "!9gag",
        "ru": "!9gag"
    },
    "examples": {
        "en": [
            "!9gag"
        ],
        "ru": [
            "!9gag"
        ]
    },
    "adapters": []
}


def get_answer(message, lang, bot, options):
    response = json.loads(requests.get('http://api-9gag.herokuapp.com').text)
    random_num = random.randint(0, len(response) - 1)
    post_text = response[random_num]['title']
    post_url = response[random_num]['src']
    bot.send_message(
        message_text=post_text,
        message_photos=[download_photo(post_url)],
        sender_id=message['sender_id'],
        sender_type=message['sender_type']
    )
    return True