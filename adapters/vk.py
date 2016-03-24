"""
# Adapter for receiving and sending messages by
# Telegram Bot API
name: telegram
description: "Adapter for connecting to Telegram"
config:
  LEONARD_TELEGRAM_TOKEN: ''
"""

import time
import json
import requests
from leonard.adapter import IncomingMessage
from leonard.utils import logger

VK_API_URL = "https://api.vk.com/method/{}?v=5.41"


def get_messages(bot):
    token = bot.config.get('LEONARD_VK_TOKEN')
    # Get last message id
    url = VK_API_URL.format('messages.get')
    response = requests.get(url, params={'access_token': token,
                                         'count': 1})
    message_data = json.loads(response.text)['response']['items'][0]
    last_message_id = message_data['id']
    while True:
        response = requests.get(url, params={'access_token': token,
                                             'count': 50,
                                             'last_message_id': last_message_id})
        messages = json.loads(response.text)['response']['items']
        for message in messages:
            if 'body' in message:
                message_text = message['body']
            else:
                message_text = ''
            vk_id = message['user_id']
            # Prepare variables to save it in DB
            variables = {
                'last_message': message,
                'adapter': 'vk'
            }
            # If user send localition, save it to message object and
            # DB variables to use location later
            if 'geo' in message:
                location = list(map(float, message['geo']['coordinates'].split()))
                variables['location'] = location
            else:
                location = None
            # Leonard iterating with message with 'for in', so our function
            # is generator of IncomingMessage objects.
            yield IncomingMessage(
                adapter_id='vk' + str(message['user_id']),
                text=message_text,
                attachments=[],
                location=location,
                variables=variables
            )
            last_message_id = message['id']
        time.sleep(5)


def send_message(message, bot):
    token = bot.config.get('LEONARD_VK_TOKEN')
    url = VK_API_URL.format('messages.send')
    params = {
        'access_token': token,
        'message': message.text,
        'peer_id': message.recipient.data['adapter_id'].lstrip('vk'),
        'notification': 1
    }

    if message.location:
        params['lat'] = message.location[0]
        params['long'] = message.location[1]

    response = requests.get(url, params=params)
