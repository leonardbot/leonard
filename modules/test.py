from sheldon import send_message

module_config = [
    {
        "name": "test",
        "public_name": {
            "en": "Test",
            "ru": "Тест"
        },
        "description": {
            "en": "Check bot for basic operability",
            "ru": "Проверка бота на общую работоспособность"
        },
        "regexps": {
                "en": [
                    "!t(est)?"
                ],
                "ru": [
                    "!т(ест)?"
                ]
        },
        "command_format": {
            "en": "!test",
            "ru": "!тест"
        },
        "examples": {
            "en": [
                "!test",
                "!t"
            ],
            "ru": [
                "!тест",
                "!т"
            ]
        },
        "adapters": [],
        "options": {}
    }
]



def get_answer(message):
    send_message(
        message_text="Тест пройден. Cообщение: '{text}' от {name}".format(
            text=message["message"],
            name=message["name"]
        )
    )
    return True