import json
import giphypop
from utils.download_photo import download_photo

module_config = {
    "name": "gif",
    "public_name": {
        "en": "Gif",
        "ru": "Гифка"
    },
    "description": {
        "en": "Random gif",
        "ru": "Рандомная гифка"
    },
    "regexps": {
            "en": [
                "!gif ?(.+)?"
            ],
            "ru": [
                "!гифка ?(.+)?"
            ]
    },
    "command_format": {
        "en": "!gif",
        "ru": "!гифка"
    },
    "examples": {
        "en": [
            "!gif"
        ],
        "ru": [
            "!гифка"
        ]
    },
    "adapters": []
}


def get_answer(message, lang, bot, options):
    giphy = giphypop.Giphy()
    if options:
        gif = giphy.screensaver(tag=options[0])
    else:
        gif = giphy.screensaver()

    bot.send_message(
        message_photos=[download_photo(gif.media_url)],
        sender_id=message['sender_id'],
        sender_type=message['sender_type']
    )
    return True