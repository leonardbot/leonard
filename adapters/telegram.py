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

TELEGRAM_API_URL = 'https://api.telegram.org/bot{token}/{method}'


def get_messages(bot):
    # Get bot token
    token = bot.config.get('LEONARD_TELEGRAM_TOKEN', '')
    if not token:
        logger.critical_message('LEONARD_TELEGRAM_TOKEN not set')
        return []

    # Try connect to Telegram
    response = json.loads(requests.get(
        TELEGRAM_API_URL.format(token=token, method='getMe')
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
            TELEGRAM_API_URL.format(token=token, method='getUpdates'),
            data={'offset': last_update_id + 1}
        ).text)
        for event in response['result']:
            last_update_id = event['update_id']
            if 'message' in event:
                message = event['message']
                # May be user didn't provided text of message, so message['text']
                # is empty.
                if 'text' in message:
                    message_text = message['text']
                else:
                    message_text = ''
                # Check, is first_name and last_name set in
                # user's telegram profile. If not, save None.
                if 'first_name' in message['from']:
                    first_name = message['from']['first_name']
                else:
                    first_name = None
                if 'last_name' in message['from']:
                    last_name = message['from']['last_name']
                else:
                    last_name = None
                # Prepare variables to save it in DB
                variables = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'last_message': message,
                    'adapter': 'telegram'
                }
                # If user send localition, save it to message object and
                # DB variables to use location later
                if 'location' in message:
                    location = (
                        message['location']['latitude'],
                        message['location']['longitude']
                    )
                    variables['location'] = location
                else:
                    location = None
                # Leonard iterating with message with 'for in', so our function
                # is generator of IncomingMessage objects.
                yield IncomingMessage(
                    adapter_id=message['from']['id'],
                    text=message_text,
                    attachments=[],
                    location=location,
                    variables=variables
                )
        time.sleep(1)
    return []


def send_message(message, bot):
    logger.info_message('Sending message', message)

    data = {
        'chat_id': message.recipient.data['adapter_id'],
        'text': message.text
    }

    # Add buttons to message data
    if message.buttons:
        data['reply_markup'] = json.dumps({
            'keyboard': message.buttons,
            'one_time_keyboard': True
        })
    else:
        data['reply_markup'] = json.dumps({
            'hide_keyboard': True
        })

    # There is special variable for hiding previews in Telegram
    if message.variables.get('telegram_hide_preview', False):
        data['disable_web_page_preview'] = True

    response = requests.get(TELEGRAM_API_URL.format(
        token=bot.config.get('LEONARD_TELEGRAM_TOKEN', ''),
        method='sendMessage'
    ), data=data)

    if not json.loads(response.text)['ok']:
        logger.error_message(
            'Problems with sending message: {}'.format(response.text)
        )

    # Now send attachments from message
    for attachment in message.attachments:
        data = {
            'chat_id': message.recipient.data['adapter_id']
        }
        response = requests.get(TELEGRAM_API_URL.format(
            token=bot.config.get('LEONARD_TELEGRAM_TOKEN', ''),
            method='send' + attachment.type.capitalize()
        ), data=data, files={
            attachment.type: (attachment.path, open(attachment.path, 'rb').read())
        })

        if not json.loads(response.text)['ok']:
            logger.error_message(
                'Problems with sending message: {}'.format(response.text)
            )
