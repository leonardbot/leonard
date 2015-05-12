from json import dumps

# Basic config for modules
modules_config = [
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
        "adapters": []
    }
]
modules_config_file = open('config/modules.json', 'w')
modules_config_file.write(dumps(modules_config))
modules_config_file.close()
