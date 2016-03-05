"""
name: notes
description: saving user's notes
priority: 150
"""

import time
import leonard
import leonard.utils


def add_note(user, note_text):
    if len(note_text) > 1000:
        note_text = note_text[:1000]
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
            text=message.locale.enter_note(bot)
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
    no_text = 'There are nothing to note.'
    saved = 'Note saved 👍'

    def enter_note(self, bot):
        answer = ('What do you want to note? 📝\n(if note will be very long, ' +
                  'I will can save only first 1000 symbols)\n\n' +
                  bot.get_locale('utils', self.language_code).question_explanation)
        return answer


class RussianLocale:
    language_code = 'ru'
    no_text = 'Здесь нечего записывать.'
    saved = 'Заметка сохранена 👍'

    def enter_note(self, bot):
        answer = ('Что ты хочешь записать? 📝 (если заметка будет очень ' +
                  'большая, я смогу сохранить только первые 1000 символов)\n\n' +
                   bot.get_locale('utils', self.language_code).question_explanation)
        return answer
