from json import dumps

# Basic config for modules
modules_config = [
    {
        "name": "test",
        "public_name": "Test",
        "description": "Проверка общей работоспособности бота",
        "regexps": [
            "!(тест|test|т|t)"
        ],
        "command_format": "!тест",
        "examples": [
            "!тест",
            "!test",
            "!т"
        ]
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