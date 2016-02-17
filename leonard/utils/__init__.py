REPLACE_WORDS = [',', '.', '?', '!', '(',
                 ')', ':', '"', '/', ';',
                 "'s", 'bot', 'leonard',
                 'hey', 'hi', 'leo', 'i need',
                 'i want', 'tell me', 'do you know',
                 'you know', 'how', 'what', 'who',
                 'how is', 'what is', 'who is', 'is',
                 'please', 'but', 'эй', 'бот', 'ок',
                 'леонард', 'мне нужно', 'я хочу',
                 'расскажи мне', 'скажи мне',
                 'ты знаешь', 'как', 'что', 'когда']


def normalize_message(message_text):
    """
    Normalize message to make catching hooks easier.

    "Hey, Leonard, who is Taylor Swift" => "taylor swift"

    :param message_text: str, original message text
    :return: str, normalizated message text
    """
    # First, make all letters lower.
    # "hey, leonard, who is taylor swift"
    message_text = message_text.lower()

    # Delete all words or symbols, that not effecting
    # on user's message
    # "          taylor swift"
    for word in REPLACE_WORDS:
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
