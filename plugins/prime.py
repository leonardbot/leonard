"""
name: prime
description: Hooks for working with prime numbers
priority: 150
"""

import leonard
import leonard.utils


def is_prime(number):
    if number == 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True


def all_primes(n):
    """
    Implementation of Eratosthenes alg
    """
    primes = [2]
    a = []
    prime = 1
    i = 3
    while (i <= n):
        if  i not in a:
            primes.append(i)
            prime += 1
            j = i
            while (j <= (n / i)):
                a.append(i * j)
                j += 1
        i += 2
    return primes


@leonard.hooks.message(['prime (\d+)', '(\d+) in primes', 'простое (\d+)'])
def is_prime_message(message, bot):
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


@leonard.hooks.keywords([['primes'], ['простые']])
def primes_list_message(message, bot):
    # Find all digits in message, may be its limit of primes
    numbers = leonard.utils.find_numbers(message.normalizated_text)
    # If user didn't define limits, print all prime numbers from 1 to 1000
    if not numbers:
        a = 1
        b = 1000
    else:
        # a, b should be limits of primes number list.
        a = min(numbers)
        b = max(numbers)
        # If user defined only one number, let's say that it was max limit,
        # so min limit will be 1
        if a == b:
            a = 1

        # If b is still 1, return, is number 1 prime
        if b == 1:
            answer = leonard.OutgoingMessage(
                recipient=message.sender,
                text=message.locale.isnt_prime.format(number)
            )
            bot.send_message(answer)
            return

    if a - b > 5000 or b > 1000000:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.too_big
        )
        bot.send_message(answer)
        return

    # Calculate all prime numbers from 1 to b
    prime_numbers = all_primes(b)
    # Than find numbers that in [a, b]
    numbers_range = []
    for num in prime_numbers:
        if num >= a:
            numbers_range.append(num)
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.primes.format(a, b, ' '.join(map(str, numbers_range)))
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'
    too_big = "It's too big for me"
    is_prime = '{} number is prime'
    isnt_prime = "{} number isn't prime"
    primes = "Prime numbers from {} to {}:\n\n{}"


class RussianLocale:
    language_code = 'ru'
    too_big = 'Это слишком много для меня'
    is_prime = 'Число {} простое'
    isnt_prime = 'Число {} не простое'
    primes = "Простые числа от {} до {}:\n\n{}"
