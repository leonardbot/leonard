"""
name: reminders
description: save reminders and notificate about it
priority: 300
"""

import schedule
import leonard
from leonard.utils import utc

time_variants = [
    (('tomorrow', 'next day', 'завтра', 'следующий день'),
     lambda current_time: current_time + 24 * 3600),
]


def create_notification(bot, message, ross_data, reminder_time):
    bot.storage.set_json('reminders',
                         bot.storage.get_json('reminders', []) +
                             [[message.sender.data['adapter_id'],
                              reminder_time,
                              message.locale.reminder.format(ross_data['query'])]
                             ]
                        )
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.created
    )
    bot.send_message(answer)


@leonard.hooks.ross(type='reminders', subtype='create')
def create_reminder_message(message, bot):
    ross_data = message.variables['ross']
    if not ross_data['query']:
        return
    # notification time = current time + time after
    time_after = ross_data.get('time_after')
    if time_after:
        create_notification(bot, message, ross_data, utc() + time_after)
        return
    # notification time = time in
    time_in = ross_data.get('time_in')
    if time_in:
        for (time_names, func) in time_variants:
            if time_in in time_names:
                create_notification(bot, message, ross_data, func(utc()))
                return


@leonard.hooks.interval(schedule.every(5).seconds)
def reminders_tick(bot):
    reminders = bot.storage.get_json('reminders')
    if not reminders:
        return
    i = 0
    while i < len(reminders):
        if utc() >= reminders[i][1]:
            recipient = bot.database.find_by_adapter_id(reminders[i][0])
            answer = leonard.OutgoingMessage(
                recipient=recipient,
                text=reminders[i][2]
            )
            bot.send_message(answer)
            reminders.pop(i)
        i += 1
    reminders = bot.storage.set_json('reminders', reminders)


class EnglishLocale(leonard.locale.EnglishLocale):
    language_code = 'en'
    created = 'I created reminder 👍\n\nI will send notification to you.'
    reminder = 'Reminder: «{}»'


class RussianLocale(leonard.locale.RussianLocale):
    language_code = 'ru'
    created = 'Я создал напоминание 👍\n\nЯ отправлю уведомление о нем.'
    reminder = 'Напоминание: «{}»'
