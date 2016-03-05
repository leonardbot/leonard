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
    if not user.data['notes']:
        note_id = 1
    else:
        note_id = max(user.data['notes'], key=lambda x: x['id'])['id'] + 1
    user.data['notes'].append({'id': note_id,
                               'datetime': leonard.utils.utc(),
                               'text': note_text})
    user.update()


def get_last_notes(user, num):
    user_notes = sorted(user.data['notes'], key=lambda x: x['datetime'],
                        reverse=True)
    return user_notes[-num:]


def get_note_by_id(user, note_id):
    for note in user.data['notes']:
        if note_id == note['id']:
            return note


def get_all_notes(user, ascending=False):
    if ascending:
        return sorted(user.data['notes'], key=lambda x: x['datetime'])
    else:
        return sorted(user.data['notes'], key=lambda x: x['datetime'],
                      reverse=True)


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


@leonard.hooks.ross(type='notes', subtype='view', position='last')
def last_notes_message(message, bot):
    last_notes = get_last_notes(message.sender, message.variables['ross']['number'])
    if len(last_notes) == 0:
        answer_text = message.locale.no_notes
    elif len(last_notes) == 1:
        last_note = last_notes[0]
        answer_text = (message.locale.last_note +
                       message.locale.note.format(
                           last_note['id'],
                           last_note['datetime'],
                           last_note['text']
                       ))
    else:
        answer_text = message.locale.last_notes
        for note in last_notes:
            answer_text += message.locale.note.format(
                note['id'],
                note['datetime'],
                note['text']
            )

    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=answer_text
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'
    no_text = 'There are nothing to note.'
    saved = 'Note saved 👍'
    no_notes = ("I don't know your notes yet. 🤔\n"
                "Send 'note' or 'note that ...' to create one.")
    last_note = "Your last note: 📝\n\n"
    last_notes = 'Your last notes: 📝\n\n'
    note = '#{}, {} - «{}»\n'

    def enter_note(self, bot):
        answer = ('What do you want to note? 📝\n(if note will be very long, ' +
                  'I will can save only first 1000 symbols)\n\n' +
                  bot.get_locale('utils', self.language_code).question_explanation)
        return answer


class RussianLocale:
    language_code = 'ru'
    no_text = 'Здесь нечего записывать.'
    saved = 'Заметка сохранена 👍'
    no_notes = ("Я пока не знаю твоих заметок. 🤔\n"
                "Отправь 'запиши' или 'запиши что ...', "
                "если хочешь создать новую.")
    last_note = 'Твоя последняя заметка: 📝\n\n'
    last_notes = 'Твои последние заметки: 📝\n\n'
    note = '#{}, {} - «{}»\n'


    def enter_note(self, bot):
        answer = ('Что ты хочешь записать? 📝\n(если заметка будет очень ' +
                  'большая, я смогу сохранить только первые 1000 символов)\n\n' +
                   bot.get_locale('utils', self.language_code).question_explanation)
        return answer
