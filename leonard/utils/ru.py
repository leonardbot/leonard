VOWEL_ENDS = (
    'ая', 'ую', 'ые', 'ой', 'ый', 'ий', 'ое', 'ее',
    'ю', 'у', 'ешь', 'ёшь', 'ишь', 'ет', 'ёт', 'ит',
    'ем', 'ём', 'им', 'ете', 'ёте', 'ите', 'ют', 'ат', 'ят',
    'и', 'а', 'ы', 'е', ''
)


def vowel_ends(base_word):
    """
    Add different vowel ends to word.
    Example: 'красив' => ['красивая', 'красивую', 'красивые'...]

    :param base_word: word root, like 'погод', 'красив'
    :return: list of new words
    """
    words = []
    for vowel_end in VOWEL_ENDS:
        words.append(base_word + vowel_end)
    return words
