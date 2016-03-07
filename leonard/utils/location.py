# -*- coding: utf-8 -*-

"""
Functions for getting information about user's location

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015-2016
"""
import json
import requests

MAPBOX_GEOCODE_API = ('https://api.mapbox.com/geocoding/v5/mapbox.places/'
                      '{},{}.json?access_token={}')
TIMEZONEDB_API = 'http://api.timezonedb.com/?lat={}&lng={}&format=json&key={}'


def get_place_data(coordinates, bot):
    response = requests.get(MAPBOX_GEOCODE_API.format(
        coordinates[1], coordinates[0], bot.config.get('LEONARD_MAPBOX_TOKEN')
    ))
    place_data = json.loads(response.text)
    # Get nearest place (for example, street)
    nearest_place = place_data['features'][0]['text']

    for feature in place_data['features']:
        if feature['id'].startswith('place'):
            city_name = feature['text']
            break
    else:
        city_name = None

    for feature in place_data['features']:
        if feature['id'].startswith('postcode'):
            postcode = feature['text']
            break
    else:
        postcode = None

    for feature in place_data['features']:
        if feature['id'].startswith('country'):
            country = feature['text']
            if 'short_code' in feature:
                country_code = feature['short_code']
            else:
                country_code = feature['properties']['short_code']
            break
    else:
        contry = None
        country_code = None

    return {'nearest_place': nearest_place, 'city_name': city_name,
            'postcode': postcode, 'country': country,
            'country_code': country_code}


def get_timezone(coordinates, bot):
    response = requests.get(TIMEZONEDB_API.format(
        coordinates[0], coordinates[1],
        bot.config.get('LEONARD_TIMEZONEDB_TOKEN')
    ))
    timezone_data = json.loads(response.text)
    return {'timezone_name': timezone_data['zoneName'],
            'utc_offset': int(timezone_data['gmtOffset'])}
