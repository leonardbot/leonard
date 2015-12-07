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

TELEGRAM_API_URL = 'https://api.telegram.org/bot{token}/{method}?{params}'


def track_message(message):
    """
    Track message in Botan.io

    :param message: dict, message from telegram
    """
    message['adapter'] = 'telegram'


def get_messages(bot):
    # Get bot token
    token = bot.config.get('LEONARD_TELEGRAM_TOKEN', '')
    if not token:
        logger.critical_message('LEONARD_TELEGRAM_TOKEN not set')
        return []

    # Try connect to Telegram
    response = json.loads(requests.get(
        TELEGRAM_API_URL.format(
            token=token, method='getMe', params=''
        )
    ).text)
    if not response['ok']:
        logger.critical_message(
            'Problems while connecting to Telegram: {}'.format(response)
        )
        exit()

    # Start getting messages
    last_update_id = -1
    while True:
        response = json.loads(requests.get(
            TELEGRAM_API_URL.format(
                token=token, method='getUpdates',
                params='offset={}'.format(last_update_id + 1)
            )
        ).text)
        for event in response['result']:
            last_update_id = event['update_id']
            if 'message' in event:
                message = event['message']
                # Track message
                track_message(message)
                yield IncomingMessage(
                    adapter_id='telegram-{}'.format(message['from']['id']),
                    text=message['text'],
                    attachments=[],
                    variables={
                        'id': message['from']['id'],
                        'first_name': message['from']['first_name'],
                        'last_name': message['from']['last_name'],
                        'adapter': 'telegram'
                    }
                )
        time.sleep(1)
    return []


def send_message(message, bot):
    response = requests.get(TELEGRAM_API_URL.format(
        token=bot.config.get('LEONARD_TELEGRAM_TOKEN', ''),
        method='sendMessage', params='chat_id={}&text={}'.format(
            message.recipient.data['id'],
            message.text
        )
    ))
    if not json.loads(response.text)['ok']:
        logger.error_message(
            'Problems with sending message: {}'.format(response)
        )