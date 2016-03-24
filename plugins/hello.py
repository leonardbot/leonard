"""
# Config (valid YAML document) must be at __doc__.
name: hello     # Name of plugin, lowercase, match with
                # file or package name.
description: "Example plugin for testing bot."
priority: 5
config:                            # Config variable that needed to set
  LEONARD_SOME_API_KEY: '123'      # in environment.
                                   # You must set default values after colon.
"""

import leonard
import schedule


@leonard.hooks.message([''])
def hello_message(message, bot):
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.hello_message,
        attachments=[]
    )
    bot.send_message(answer)


@leonard.hooks.interval(schedule.every(5).minutes)
def hello_interval(bot):
    leonard.logger.info_message(bot.get_locale('hello', 'en').interval_message)


class EnglishLocale(leonard.locale.EnglishLocale):
    language_code = 'en'
    hello_message = 'Hi!'
    interval_message = 'Hello from hello module'


class RussianLocale(leonard.locale.RussianLocale):
    language_code = 'ru'
    hello_message = 'Привет!'
