"""
name: prime
description: Hooks for working with prime numbers
priority: 150
"""

import leonard


def is_prime(number):
    if number == 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True


@leonard.hooks.message(['prime (\d+)', 'простое (\d+)'])
def send_answer(message, bot):
    number = int(message.variables['regex_match'][0])
    if number > 100000000000:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.too_big
        )
        bot.send_message(answer)
        return
    if is_prime(number):
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.is_prime.format(number)
        )
        bot.send_message(answer)
    else:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.isnt_prime.format(number)
        )
        bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'
    too_big = 'Number is too big'
    is_prime = '{} number is prime'
    isnt_prime = "{} number isn't prime"


class RussianLocale:
    language_code = 'ru'
    too_big = 'Число слишком большое'
    is_prime = 'Число {} простое'
    isnt_prime = 'Число {} не простое'
