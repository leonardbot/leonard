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
    if not 'notes' in user.data:
        return []
    user_notes = sorted(user.data['notes'], key=lambda x: x['datetime'],
                        reverse=True)
    print(user_notes, num)
    return user_notes[:num]


def get_note_by_id(user, note_id):
    for note in user.data['notes']:
        if note_id == note['id']:
            return note


def get_all_notes(user, ascending=False):
    if not 'notes' in user.data:
        return []
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
                       ) + '\n' + message.locale.how_see_all)
    else:
        answer_text = message.locale.last_notes
        for note in last_notes:
            answer_text += message.locale.note.format(
                note['id'],
                note['datetime'],
                note['text']
            )
        answer_text += '\n'
        answer_text += message.locale.how_see_all

    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=answer_text
    )
    bot.send_message(answer)


@leonard.hooks.ross(type='notes', subtype='view', position='id')
def notes_by_id_message(message, bot):
    note = get_note_by_id(message.sender, message.variables['ross']['id'])
    if not note:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.no_note
        )
        bot.send_message(answer)
        return
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.note.format(
            note['id'], note['datetime'], note['text']
        )
    )
    bot.send_message(answer)


@leonard.hooks.ross(type='notes', subtype='view', position='all')
def all_notes_message(message, bot):
    if message.sender.data.get('all_notes_buffer', []):
        message.sender.data['all_notes_buffer'] = []
    message.sender.data['all_notes_buffer'] = get_all_notes(message.sender,
                                                            ascending=True)
    show_notes = []
    # Get last 10 notes
    for i in range(10):
        if message.sender.data['all_notes_buffer']:
            show_notes.append(message.sender.data['all_notes_buffer'].pop())
        else:
            break
    message.sender.update()
    if not show_notes:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.no_notes
        )
        bot.send_message(answer)
        return
    answer_text = message.locale.all_notes
    for note in show_notes:
        answer_text += message.locale.note.format(
            note['id'],
            bot.get_locale('utils', message.sender.data['language']).format_datetime(
                note['datetime'], message.sender.data.get('utc_offset', 0)
            ),
            note['text']
        )
    answer_text += '\n'
    answer_text += message.locale.how_see_more
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=answer_text,
        buttons=[[message.locale.more], [message.locale.exit]]
    )
    bot.ask_question(answer, all_notes_callback, 'notes')


def all_notes_callback(message, bot):
    # If message is not 'more', so ignore it
    if message.text != message.locale.more.lower():
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.how_see_more
        )
        bot.ask_question(answer, all_notes_callback, 'notes')
        return
    if not message.sender.data['all_notes_buffer']:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.no_more_notes
        )
        bot.send_message(answer)
        return
    show_notes = []
    for i in range(10):
        if message.sender.data['all_notes_buffer']:
            show_notes.append(message.sender.data['all_notes_buffer'].pop())
        else:
            break
    message.sender.update()
    answer_text = ''
    for note in show_notes:
        answer_text += message.locale.note.format(
            note['id'],
            note['datetime'],
            note['text']
        )
    answer_text += '\n'
    answer_text += message.locale.how_see_more
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=answer_text,
        buttons=[[message.locale.more], [message.locale.exit]]
    )
    bot.ask_question(answer, all_notes_callback, 'notes')


class EnglishLocale:
    language_code = 'en'
    no_text = 'There are nothing to note.'
    saved = 'Note saved 👍\n\nYou can view it by sending "last note"'
    no_notes = ("I don't know your notes yet. 🤔\n"
                "Send 'note' or 'note that ...' to create one.")
    no_more_notes = "No more notes, that's all. 🙁"
    no_note = "I din't found note with this id 🙁"
    last_note = "Your last note: 📝\n\n"
    last_notes = 'Your last notes: 📝\n\n'
    all_notes = 'All your notes:\n\n'
    more = 'More'
    exit = 'Exit'
    how_see_more = ('If you want to read more your notes, just '
                    'send "more". You can send "exit" to quit. ')
    how_see_all = "Send 'all notes' if you want to see more notes."
    note = '#{}, {} - «{}»\n'

    def enter_note(self, bot):
        answer = ('What do you want to note? 📝\n\n(if note will be very long, ' +
                  'I will can save only first 1000 symbols)\n\n' +
                  bot.get_locale('utils', self.language_code).question_explanation)
        return answer


class RussianLocale:
    language_code = 'ru'
    no_text = 'Здесь нечего записывать.'
    saved = ('Заметка сохранена 👍\n\nОтправь "последняя заметка", '
             'если хочешь просмотреть ее')
    no_notes = ("Я пока не знаю твоих заметок. 🤔\n"
                "Отправь 'запиши' или 'запиши что ...', "
                "если хочешь создать новую.")
    no_more_notes = "Больше нет заметок, это всё. 🙁"
    no_note = "Я не нашел заметку с этим номером 🙁"
    last_note = 'Твоя последняя заметка: 📝\n\n'
    last_notes = 'Твои последние заметки: 📝\n\n'
    all_notes = 'Все твои заметки:\n\n'
    more = 'Дальше'
    exit = 'Выйти'
    how_see_more = ('Если ты хочешь посмотреть больше заметок, '
                    'отправь "дальше". Если ты узнал, что тебе нужно - '
                    'можно отправить "выйти", чтобы закончить просмотр.')
    how_see_all = 'Чтобы посмотреть все заметки, отправьте "все заметки".'
    note = '#{}, {} - «{}»\n'


    def enter_note(self, bot):
        answer = ('Что ты хочешь записать? 📝\n\n(если заметка будет очень ' +
                  'большая, я смогу сохранить только первые 1000 символов)\n\n' +
                   bot.get_locale('utils', self.language_code).question_explanation)
        return answer
