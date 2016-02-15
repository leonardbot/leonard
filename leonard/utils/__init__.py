from leonard.hooks import REPLACE_SYMBOLS


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
