# -*- coding: utf-8 -*-

"""
Different functions for making bot better

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015
"""
import os
import os.path
import time
import random
import requests

REPLACE_SYMBOLS = [
                   ',', '.', '?', '!', '(',
                   ')', ':', '"', ';'
                  ]

REPLACE_WORDS = [
                 "'s", 'bot', 'leonard', 'hello',
                 'hey', 'hi', 'leo', 'i need',
                 'i want', 'tell me', 'do you know',
                 'you know', 'how', 'what', 'who',
                 'how is', 'what is', 'who is', 'is',
                 'me', 'say', 'sorry', 'can', 'you', 'give',
                 'need', 'for', 'please', 'but', 'about',
                 'эй', 'бот', 'ок', 'леонард', 'дай', 'подай',
                 'мне нужно', 'я хочу', 'расскажи мне',
                 'скажи мне', 'ты знаешь', 'как', 'что',
                 'мне', 'я', 'можешь', 'когда', 'про',
                 'о'
                ]


class NextHook(BaseException):
    """
    Exception that raises plugin if there is no data for user.
    """
    pass


def clean_message(message_text):
    """
    Delete punctuation marks and lowercase message text

    "Hey, Leonard, who is Taylor Swift" => "hey leonard who is taylor swift"

    :param message_text: str, original message
    :return: str, cleaned message_text
    """
    # First, make all letters lower.
    # "hey, leonard, who is taylor swift"
    message_text = message_text.lower()

    # Delete punctuation marks
    for symbol in REPLACE_SYMBOLS:
        message_text = message_text.replace(symbol, ' ')

    # Delete extra spaces
    message_text = ' '.join(message_text.split())

    return message_text

def normalize_message(message_text):
    """
    Normalize message to make catching hooks easier.

    "Hey, Leonard, who is Taylor Swift" => "taylor swift"

    :param message_text: str, cleaned message text
    :return: str, normalizated message text
    """
    # Delete all words or symbols, that not effecting
    # on user's message
    # "          taylor swift"

    # Add extra spaces to begin and end of message to make
    # deleting words easier
    message_text = " " + message_text + " "

    for word in REPLACE_WORDS:
        # Word should be separate
        word = " " + word + " "
        message_text = message_text.replace(word, '')

    # If there are extra spaces, delete it
    message_text = ' '.join(message_text.split())

    return message_text


def keywords_from_words(words):
    """
    Generate a list for keywords hook from single words.
    Keywords hook accepting list of variants where variants is list too.
    So keyword hook matching when all words from one or more variants
    contains in a message. This function generating list of variants from
    list of possible words.

    ['weather', 'forecast'] => [['weather'], ['forecast']]

    :param words: list of str, possible words
    :return: list of list of variants, ready argument for keywords hook
    """
    return list(map(lambda word: [word], words))


def pop_words(message_text, words):
    """
    Remove some words from message_text

    'How you doing?'; ['how', 'you'] => 'doing'

    :param message_text: str, query text
    :param words: list of str, words that needed to pop
    :return: str without words and escaping symbols
    """
    # Normalize message
    message_text = message_text.lower()
    for sym in REPLACE_SYMBOLS:
        message_text = message_text.replace(sym, '')
    # Delete needed words
    message_words = []
    for word in message_text.split():
        if word not in words:
            message_words.append(word)
    return ' '.join(message_words)


def download_file(url, plugin_name):
    """
    Download file from url and save it

    :param url: file url
    :param plugin_name: str, name of plugin that downloading file
    :return: absolute path to file
    """
    response = requests.get(url)
    # Create folder for data
    try:
        os.mkdir('data/' + plugin_name)
    except OSError:
        # If folder already existing, just pass
        pass
    file_extension = response.url.split('.')[-1].rstrip('/')
    file_name = str(time.time()) + '_' + str(random.randint(1, 1000000000))
    file_path = 'data/' + plugin_name + '/' + file_name + '.' + file_extension
    downloaded_file = open(file_path, 'wb')
    downloaded_file.write(response.content)
    downloaded_file.close()
    return os.path.abspath(file_path)
