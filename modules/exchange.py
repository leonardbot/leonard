import requests
from pyquery import PyQuery

module_config = {
    "name": "exchange",
    "public_name": {
        "en": "Exchange",
        "ru": "Конвертер валют"
    },
    "description": {
        "en": "Exchange dollars/euro/rubles to dollars/euro/rubles",
        "ru": "Перевод долларов/евро/рублей в доллары/евро/рубли"
    },
    "regexps": {
            "en": [
                "!((to )?(dollar|euro|ruble)(s)? (\d+) (dollar|euro|ruble)(s)?|dollar|ruble|euro)"
            ],
            "ru": [
                "!((в )?(рубл|евро|доллар)(ы|и|а|ов|ей)? (\d+) (рубл|евро|доллар)(ы|и|а|ов|ей)?|рубл|доллар|евро)"
            ]
    },
    "command_format": {
        "en": "!to <needed currency> <value> <currency>",
        "ru": "!в <нужная валюта> <количество> <исходная валюта>"
    },
    "examples": {
        "en": [
            "!to dollars 5 euro",
            "!euro"
        ],
        "ru": [
            "!в доллары 5 рублей",
            "!рубль"
        ]
    },
    "adapters": []
}

small_names_of_currency = {
    'en': {
        'dollar': 'usd',
        'euro': 'eur',
        'ruble': 'rub'
    },
    'ru': {
        'доллар': 'usd',
        'евро': 'eur',
        'рубл': 'rub'
    }
}
full_names_of_currency = {
    'en': {
        'usd': 'dollar(s)',
        'eur': 'euro',
        'rub': 'ruble'
    },
    'ru': {
        'usd': 'dollar',
        'eur': 'euro',
        'rub': 'ruble'
    }
}
incorrect_number_message = {
    'en': 'Enter correct number.',
    'ru': 'Введите корректное число.'
}


def send_incorrect_number_message(bot, message):
    bot.send_message(
        message_text=incorrect_number_message[bot.language],
        sender_id=message['sender_id'],
        sender_type=message['sender_type']
    )


def get_exchange_rate(amount, from_currency, to_currency):
    url = 'http://www.google.com/finance/converter?a={}&from={}&to={}'
    response = requests.get(
        url.format(str(amount), from_currency, to_currency)
    ).text
    get_result_query = '.g-doc form #currency_converter_result span'
    result = PyQuery(response)(get_result_query).text().split(' ')[0]
    return result


def get_answer(message, lang, bot, options):
    if options[0] in small_names_of_currency[bot.language]:
        from_currency = small_names_of_currency[bot.language][options[0]]
        if from_currency == 'usd':
            to_currency = 'eur'
            result_message = "{} {}"
        else:
            to_currency = 'usd'
            result_message = "{} {}"
        bot.send_message(
            message_text=result_message.format(
                get_exchange_rate(1, from_currency, to_currency),
                to_currency.upper()
            ),
            sender_id=message['sender_id'],
            sender_type=message['sender_type']
        )
        return True

    try:
        currency_value = int(options[4])
    except TypeError:
        send_incorrect_number_message(bot, message)
        return False
    except ValueError:
        send_incorrect_number_message(bot, message)
        return False
    else:
        to_currency = small_names_of_currency[bot.language][options[2]]
        from_currency = small_names_of_currency[bot.language][options[5]]
        bot.send_message(
            message_text='{} {} - {} {}'.format(
                str(currency_value),
                from_currency.upper(),
                get_exchange_rate(currency_value, from_currency, to_currency),
                to_currency.upper()
            ),
            sender_id=message['sender_id'],
            sender_type=message['sender_type']
        )
    return True