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
        }
    }
]
modules_config_file = open('config/modules.json', 'w')
modules_config_file.write(dumps(modules_config))
modules_config_file.close()

# Adapters config
console_adapter_config = {
    "name": "console",
    "enable": 1,
    "options": {}
}
console_adapter_config_file = open('config/adapters/console.json', 'w')
console_adapter_config_file.write(dumps(console_adapter_config))
console_adapter_config_file.close()