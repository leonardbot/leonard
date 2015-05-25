from time import sleep

module_config = {
    "name": "help",
    "public_name": {
        "en": "Help",
        "ru": "Помощь"
    },
    "description": {
        "en": "Help for all commands",
        "ru": "Помощь по всем командам"
    },
    "regexps": {
            "en": [
                "!help ?(.+)?"
            ],
            "ru": [
                "!помощь ?(.+)?"
            ]
    },
    "command_format": {
        "en": "!help <module name (optional)>",
        "ru": "!помощь <название модуля (необязательно)>"
    },
    "examples": {
        "en": [
            "!help say",
            "!help"
        ],
        "ru": [
            "!помощь !скажи",
            "!помощь"
        ]
    },
    "adapters": []
}

example_translation = {
    'en': 'Example',
    'ru': 'Пример'
}
def get_answer(message, lang, bot, options):
    modules_list = []
    # If user not choose module name, send all modules
    if options[0] is None:
        for module in bot.loaded_modules:
            module_config = bot.loaded_modules[module]['config']
            module_cmd = module_config['command_format'][lang]
            modules_list.append(
                '{name} - {desc}. {example_text}: {examples}'.format(
                    name=module_cmd,
                    desc=module_config['description'][lang].lower(),
                    example_text=example_translation[lang],
                    examples=', '.join(module_config['examples'][lang])
                )
            )
    else:
        module_config = {}
        for module in bot.loaded_modules:
            module = bot.loaded_modules[module]
            for regexp in module['regexps']:
                if regexp.match(options[0]) is not None:
                    module_config = module['config']
                    break
            if module_config:
                break
        if not module_config:
            return False

        module_cmd = module_config['command_format'][lang]
        modules_list.append(
            '{name} - {desc}. {example_text}: {examples}'.format(
                name=module_cmd,
                desc=module_config['description'][lang].lower(),
                example_text=example_translation[lang],
                examples=', '.join(module_config['examples'][lang])
            )
        )
    for module_help in modules_list:
        bot.send_message(
            message_text=module_help,
            sender_id=message['sender_id'],
            sender_type=message['sender_type']
        )
        sleep(1)
    return True