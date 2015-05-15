module_config = {
    "name": "module",
    "public_name": {
        "en": "Module",
        "ru": "Модуль"
    },
    "description": {
        "en": "Add and delete loaded modules",
        "ru": "Добавление и удаление загруженных модулей"
    },
    "regexps": {
            "en": [
                "!module (add|delete) (.+)+"
            ],
            "ru": [
                "!модуль (добавить|удалить) (.+)+"
            ]
    },
    "command_format": {
        "en": "!module <add/delete> <module name>",
        "ru": "!модуль <добавить/удалить> <имя модуля>"
    },
    "examples": {
        "en": [
            "!module delete butts",
            "!module add butts"
        ],
        "ru": [
            "!модуль удалить butts",
            "!модуль добавить butts"
        ]
    },
    "adapters": []
}

not_admin_message = {
    'en': 'You are not admin.',
    'ru': 'Вы не администратор.'
}

delete_add_words = {
    'en': ['add', 'delete'],
    'ru': ['добавить', 'удалить']
}

added_deleted_words = {
    'en': ['Added.', 'Deleted.'],
    'ru': ['Добавлено.', 'Удалено.']
}

error_message = {
    'en': "Module doesn't exists. Check it again.",
    'ru': "Модуль не существует. Проверьте название еще раз."
}

def get_answer(message, lang, bot, options):
    if bot.is_admin(message['user_id']):
        module_name = options[1]
        if options[0] == delete_add_words[lang][0]:
            if bot.add_module(module_name):
                bot.send_message(
                    message_text=added_deleted_words[lang][0],
                    sender_id=message['sender_id'],
                    sender_type=message['sender_type']
                )
            else:
                bot.send_message(
                    message_text=error_message[lang],
                    sender_id=message['sender_id'],
                    sender_type=message['sender_type']
                )
        elif options[0] == delete_add_words[lang][1]:
            if bot.delete_module(module_name):
                bot.send_message(
                    message_text=added_deleted_words[lang][1],
                    sender_id=message['sender_id'],
                    sender_type=message['sender_type']
                )
            else:
                bot.send_message(
                    message_text=error_message[lang],
                    sender_id=message['sender_id'],
                    sender_type=message['sender_type']
                )
    else:
        bot.send_message(
            message_text=not_admin_message[lang],
            sender_id=message['sender_id'],
            sender_type=message['sender_type']
        )
    return True