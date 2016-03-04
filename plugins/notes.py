"""
name: notes
description: saving user's notes
priority: 150
"""

import time
import leonard
import leonard.utils
import leonard.utils.locale as locale_utils


def add_note(user, note_text):
    user.data['notes'] = user.data.get('notes', [])
    user.data['notes'].append({'datetime': leonard.utils.utc(),
                               'text': note_text})
    user.update()


@leonard.hooks.ross(type='notes', subtype='add')
def add_note_message(message, bot):
    query = message.variables['ross']['query']
    message.sender.data['notes'] = message.sender.data.get('notes', [])
    if not query:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.enter_note
        )
        bot.ask_question(answer, add_note_callback, 'notes')
        return
    add_note(message.sender, query)
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.saved
    )
    bot.send_message(answer)


def add_note_callback(message, bot):
    query = message.uncleaned_text
    if not query:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.no_text
        )
        bot.send_message(answer)
        return
    add_note(message.sender, query)
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.saved
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'
    enter_note = ('What do you want to note?\n\n' +
                  locale_utils.get(language_code)['question_explanation'])
    no_text = 'There are nothing to note.'
    saved = 'Note saved 👍'


class RussianLocale:
    language_code = 'ru'
    enter_note = ('Что ты хочешь записать?\n\n' +
                  locale_utils.get(language_code)['question_explanation'])
    no_text = 'Здесь нечего записывать.'
    saved = 'Заметка сохранена 👍'
