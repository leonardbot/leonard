"""
name: uber
description: get taxi from Uber
priority: 300
"""

import leonard

UBER_DEEP_LINK = ('uber://?client_id={}&action=setPickup'
                  '&pickup[latitude]={}&pickup[longitude]={}'
                  '&dropoff[latitude]={}&dropoff[longitude]={}')


@leonard.hooks.ross(type='taxi', subtype='get')
def get_taxi_message(message, bot):
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.choose_location
    )
    bot.ask_question(answer, current_location_callback, 'uber')


def current_location_callback(message, bot):
    if not message.location:
        get_taxi_message(message, bot)
        return
    message.sender.data['current_uber_location'] = message.location
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.choose_destination
    )
    bot.ask_question(answer, choose_destination_callback, 'uber')


def choose_destination_callback(message, bot):
    if not message.location:
        get_taxi_message(message, bot)
        return
    # When user sending taxi destination,
    # bot shouln't save it as user's location
    message.sender.update_location_data(
        message.sender.data['current_uber_location']
    )
    current_location = message.sender.data['current_uber_location']
    destination = message.location
    uber_link = UBER_DEEP_LINK.format(bot.config.get('LEONARD_UBER_CLIENT_ID'),
                                      current_location[0], current_location[1],
                                      destination[0], destination[1])
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.open_uber.format(uber_link)
    )
    bot.send_message(answer)



class EnglishLocale(leonard.locale.EnglishLocale):
    language_code = 'en'

    @property
    def choose_location(self):
        return ('Not a problem, I can get taxi for you. 🚕\n\n' +
                'Where are you? Send me your location.\n\n' +
                self.question_explanation)

    choose_destination = 'OK. Where do you go? 🏡\nSend me location.'

    open_uber = "Open Uber app using this link:\n{}"


class RussianLocale(leonard.locale.RussianLocale):
    language_code = 'ru'

    @property
    def choose_location(self):
        return ('Не проблема, я могу заказать такси. 🚕 \n\n' +
                'Где ты сейчас? Отправь свое местоположение.\n\n' +
                self.question_explanation)

    choose_destination = ('OK. Куда ты хочешь уехать? 🏡\n'
                          'Отправь мне местоположение.')

    open_uber = "Открой приложение через ссылку:\n{}"
