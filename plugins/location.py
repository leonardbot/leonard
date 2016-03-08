"""
name: location
description: "Plugin that gives information about user's location"
priority: 100
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


@leonard.hooks.callback(lambda message: message.location is not None)
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
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text='Yayks'
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'
    location_text = ("Places around there:\n\n{}\n"
                     "Send 'where i can go' if you want to get more "
                     "information about places")
    place = '"{}" ({}) - {} meters\n'


class RussianLocale:
    language_code = 'ru'
    location_text = ("Места поблизости:\n\n{}\n"
                     "Отправь 'куда мне сходить', если хочешь выбрать место "
                     "себе по душе.")
    place = '"{}" ({}) - {} м\n'
