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
    response = vk.method('messages.get', {'last_message_id': last_message_id})
    messages = []
    for item in response['items']:
        messages.append({
            'text': item['body'],
            'time':
        })
    return [{
        "text": message,
        "time": time(),
        "sender_id": hash(getlogin()),
        "sender_name": getlogin(),
        "sender_type": None
    }]


def send_message(sender_id, sender_type,
                 message_text="", message_photos=[]):
    print("Text:", message_text)
    print("Photos:", message_photos)
    return True
