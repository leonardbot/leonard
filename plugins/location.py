"""
name: location
description: "Plugin that gives information about location based on other plugins"
priority: 100
"""
import leonard


@leonard.hooks.callback(lambda message: message.location is not None)
def location_message(message, bot):
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.base_text.format(
            str(message.location[0]),
            str(message.location[1])
        ),
        attachments=[]
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'
    base_text = "I got coordinates: {}, {}"


class RussianLocale:
    language_code = 'ru'
    base_text = "Я получил координаты: {}, {}"
