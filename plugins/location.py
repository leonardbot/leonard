"""
name: location
description: "Plugin that gives information about user's location"
priority: 250
"""
import json
import requests

import leonard
from leonard.utils import location

FOURSQUARE_SEARCH_API = ('https://api.foursquare.com/v2/venues/explore?'
                         'client_id={}&client_secret={}&ll={}'
                         '&locale={}&v=20160301')


def get_near_places(coordinates, language_code, bot, query=None):
    params = {}
    if query:
        params['query'] = query
    response = requests.get(FOURSQUARE_SEARCH_API.format(
        bot.config.get('LEONARD_FOURSQUARE_CLIENT_ID'),
        bot.config.get('LEONARD_FOURSQUARE_CLIENT_SECRET'),
        ','.join([str(coordinates[0]), str(coordinates[1])]),
        language_code
    ), params=params)
    near_places_data = json.loads(response.text)
    places = []
    for place in near_places_data['response']['groups'][0]['items']:
        categories = []
        for category in place['venue']['categories']:
            categories.append(category['name'])
        reasons = []
        for reason in place['reasons']['items']:
            reasons.append(reason['summary'])
        places.append({'name': place['venue']['name'],
                       'categories': categories,
                       'reasons': reasons,
                       'distance': place['venue']['location']['distance'],
                       'location': (place['venue']['location']['lat'],
                                    place['venue']['location']['lng']),
                       'rating': place['venue'].get('rating', None),
                       'link': 'https://foursquare.com/v/{}'.format(
                           place['venue']['id'])})
    return places


def send_place_detail(place, message, bot):
    place_answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.detail_place.format(
            name=place['name'],
            categories=', '.join(place['categories']),
            distance=place['distance'],
            reasons='\n'.join(place['reasons']),
            link=place['link']
        )
    )
    bot.send_message(place_answer)
    location_attachment = leonard.Attachment('location',
                                             lat=place['location'][0],
                                             lng=place['location'][1])
    location_answer = leonard.OutgoingMessage(
        recipient=message.sender,
        attachments=[location_attachment]
    )
    bot.send_message(location_answer)
    need_more_answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.need_more,
        buttons=[[message.locale.more], [message.locale.exit]]
    )
    bot.ask_question(need_more_answer, more_places_callback, 'location')


@leonard.hooks.callback(lambda message, bot: message.location is not None)
def location_message(message, bot):
    message.sender.update_location_data(message.location)
    places = get_near_places(message.location, message.sender.data['language'],
                             bot)
    places_text = ''
    for place in places[:5]:
        places_text += message.locale.place.format(
            place['name'], ', '.join(place['categories']), place['distance']
        )
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.location_text.format(places_text),
        attachments=[]
    )
    bot.send_message(answer)


@leonard.hooks.ross(type='places', subtype='explore')
def explore_message(message, bot):
    query = message.variables['ross']['query']
    if not query:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.choose_location(bot),
            buttons=[[message.locale.default]]
        )
        bot.ask_question(answer, explore_choose_location_callback, 'location')
        return


def explore_choose_location_callback(message, bot):
    if not (message.location or message.text == message.locale.default):
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.choose_location(bot),
            buttons=[[message.locale.default]]
        )
        bot.ask_question(answer, explore_choose_location_callback, 'location')
        return
    if message.location:
        message.sender.update_location_data(message.location)
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.choose_type(bot)
    )
    bot.ask_question(answer, explore_choose_type_callback, 'location')


def explore_choose_type_callback(message, bot):
    query = message.uncleaned_text
    if not query:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.choose_type(bot)
        )
        bot.ask_question(answer, explore_choose_type_callback, 'location')
        return
    places = get_near_places(
        message.sender.data['location'], message.sender.data['language'],
        bot, query
    )
    if not places:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.not_found
        )
        bot.send_message(answer)
        return
    message.sender.data['recommended_places'] = list(reversed(places))
    first_place = message.sender.data['recommended_places'].pop()
    message.sender.update()
    send_place_detail(first_place, message, bot)


def more_places_callback(message, bot):
    if message.text != message.locale.more:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.need_more,
            buttons=[[message.locale.more], [message.locale.exit]]
        )
        bot.ask_question(answer, more_places_callback, 'location')
        return
    if not message.sender.data['recommended_places']:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.thats_all
        )
        bot.send_message(answer)
        return
    place = message.sender.data['recommended_places'].pop()
    message.sender.update()
    send_place_detail(place, message, bot)


class EnglishLocale:
    language_code = 'en'
    location_text = ("Places around there:\n\n{}\n"
                     "Send 'where i can go' if you want to get more "
                     "information about places")
    place = '"{}" ({}) - {} meters\n'
    detail_place = ("«{name}» - {categories}\n\nDistance: {distance} meters\n"
                    "\nReasons:\n{reasons}\n\nFoursquare: {link}\n\n")
    default = 'default'
    more = 'more'
    need_more = ("You can get more places by sending 'more' or "
                 "exit using 'thanks'")
    not_found = "I didn't found anything 😬"
    thats_all = "That's all I can found 😬"
    exit = 'thanks'

    def choose_location(self, bot):
        text = ("Where are you?\n\nSend me your location, "
                "or answer 'default' if you have already sent it.\n\n" +
                bot.get_locale('utils', self.language_code).question_explanation)
        return text

    def choose_type(self, bot):
        text = ("Where do you want to go? 🤔\n\nFor example, 'to drink', "
                "'cheap place', 'restourant', 'for date'\n\n" +
                bot.get_locale('utils', self.language_code).question_explanation)
        return text


class RussianLocale:
    language_code = 'ru'
    location_text = ("Места поблизости:\n\n{}\n"
                     "Отправь 'куда мне сходить', если хочешь выбрать место "
                     "себе по душе.")
    place = '"{}" ({}) - {} м\n'
    default = 'обычное'
    detail_place = ("«{name}» - {categories}\n\nРасстояние: {distance} м\n"
                    "\nПреимущества:\n{reasons}\n\nFoursquare: {link}\n\n")
    more = 'больше'
    need_more = ("Ты можешь посмотреть следующие места, отправив 'больше' "
                 "или закончить, отправив 'все'")
    not_found = 'Я ничего не нашел 😬'
    thats_all = "Это все, что я смог найти 😬"
    exit = 'всё'

    def choose_location(self, bot):
        text = ("Где ты находишься?\n\nОтправь мне свое местоположение "
                "или отправь 'обычное', если ты уже отправлял мне его\n\n" +
                bot.get_locale('utils', self.language_code).question_explanation)
        return text

    def choose_type(self, bot):
        text = ("Куда ты хочешь пойти? 🤔\n\nНапример, 'выпить', "
                "'дешевое место', 'ресторан', 'на свидание'\n\n" +
                bot.get_locale('utils', self.language_code).question_explanation)
        return text
