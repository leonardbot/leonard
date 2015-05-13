import vk_api
import json
from time import time
from os import getlogin

adapter_config = {
    "name": "vk",
    "blocked_users_id": [],
    "admin_ids": [
        hash(getlogin())
    ]
}

try:
    vk_settings = json.loads(
        open('adapters/{adapter_name}_settings.json'.format(
            adapter_name=adapter_config['name'])
    ).read())
    vk_login = vk_settings['vk_login']
    vk_password = vk_settings['vk_password']
except FileNotFoundError:
    vk_login = input('Enter your vk login:')
    vk_password = input('Enter your vk password:')
    settings_file = open(
        'adapters/{}_settings.json'.format(
            adapter_config['name']
        ), 'w'
    )
    settings_file.write(json.dumps({
        'vk_login': vk_login,
        'vk_password': vk_password
    }))
    settings_file.close()

vk = vk_api.VkApi(vk_login, vk_password)
last_message_id = vk.method('messages.get', {
    'count': 1
})['items'][0]['id']


def get_messages():
    global last_message_id
    response = vk.method('messages.get', {'last_message_id': last_message_id})
    messages = []
    for item in response['items']:
        message = {
            'text': item['body'],
            'time': item['date'],
            'sender_id': None,
            'sender_type': None
        }
        if 'chat_id' in item:
            message['sender_id'] = item['chat_id']
            message['sender_type'] = 'chat'
        else:
            message['sender_id'] = item['user_id']
            message['sender_type'] = 'user'
        messages.append(message)
    last_message_id = response['items'][-1]['id']
    return messages


def send_message(sender_id, sender_type,
                 message_text="", message_photos=[]):
    message = {
        sender_type + '_id': sender_id,
        'message': message_text
    }
    return message
