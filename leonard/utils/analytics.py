# -*- coding: utf-8 -*-

"""
Functions for creating bot analytics

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015
"""

import json
import requests

BOTAN_URL = 'https://api.botan.io/track?token={token}&uid={uid}&name={name}'


def track_message(message, adapter, plugin, bot):
    """
    Track message in Botan.io

    :param message: dict, raw message from adapter
    :param adapter: str, adapter name
    :param plugin: str, name of plugin that proceed that message
    :param bot: Leonard object
    """
    message['adapter'] = adapter
    if adapter == 'telegram':
        user_id = message['from']['id']
    elif adapter == 'vk':
        user_id = message['user_id']
    url = BOTAN_URL.format(token=bot.config.get('LEONARD_BOTAN_TOKEN'),
                           uid=user_id, name=plugin)
    try:
        response = requests.post(
            url, data=json.dumps(message),
            headers={'Content-type': 'application/json'}
        )
        print(response.text)
        return response
    except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        return None
