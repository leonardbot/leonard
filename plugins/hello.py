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


@leonard.hooks.callback(lambda message, bot: True)
def hello_message(message, bot):
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.not_found,
        attachments=[]
    )
    bot.send_message(answer)


class EnglishLocale(leonard.locale.EnglishLocale):
    language_code = 'en'
    not_found = "Sorry, I didn't understand you. You can find all functions in https://medium.com/@sevazhidkov/leonard-bot-open-source-virtual-assistant-in-messengers-by-russian-school-students-e2b5d1aac9a5#.e2xdsduq5"


class RussianLocale(leonard.locale.RussianLocale):
    language_code = 'ru'
    not_found = "Извини, но я не понял тебя. Ты можешь посмотреть все мои функции на https://medium.com/@sevazhidkov/leonard-bot-open-source-virtual-assistant-in-messengers-by-russian-school-students-e2b5d1aac9a5#.e2xdsduq5"
