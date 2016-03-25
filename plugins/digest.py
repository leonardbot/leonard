"""
name: digest
description: send weather, news in digest to users
priority: 500
"""

import time
import schedule
import leonard
from leonard.utils import utc, user_from_data

"""
@leonard.hooks.interval(schedule.every(30).seconds)
def digest_message(bot):
    for user in bot.database.find({'adapter': bot.adapter.name,
                                   'location': {'$exists': True}}):
        if time.gmtime(utc() - user['gmt_offset']).tm_hour == 10:
            digest = leonard.OutgoingMessage(
                recipient=user_from_data(user),
                text=message.locale.digest
            )
            bot.send_message(answer)
"""

class EnglishLocale(leonard.locale.EnglishLocale):
    language_code = 'en'
    digest = 'Good morning!'


class RussianLocale(leonard.locale.RussianLocale):
    language_code = 'ru'
    digest = 'Доброе утро!'
