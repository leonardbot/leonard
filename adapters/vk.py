import vk_api
import os
from time import sleep
from requests.exceptions import ConnectionError

adapter_config = {
    "name": "vk",
    "blocked_users_id": [],
    "admin_ids": [
        91670994
    ]
}

vk_login = os.environ['VK_LOGIN']
vk_password = os.environ['VK_PASSWORD']
vk = vk_api.VkApi(vk_login, vk_password)
vk.authorization()
last_message_id = vk.method('messages.get', {
    'count': 1
})['items'][0]['id']
vk_upload = vk_api.VkUpload(vk)


def get_messages():
    global last_message_id
    try:
        response = vk.method('messages.get', {'last_message_id': last_message_id})
    except vk_api.ApiError:
        return []
    except ConnectionError:
        return []
    except vk_api.ApiHttpError:
        return []

    messages = []
    if response['items']:
        last_message_id = response['items'][-1]['id']
    for item in response['items']:
        message = {
            'text': item['body'],
            'time': item['date'],
            'sender_id': None,
            'sender_type': None,
            'user_id': item['user_id']
        }
        if 'chat_id' in item:
            message['sender_id'] = item['chat_id']
            message['sender_type'] = 'chat'
        else:
            message['sender_id'] = item['user_id']
            message['sender_type'] = 'user'
        messages.append(message)
    return messages


def send_message(sender_id, sender_type,
                 message_text="", message_photos=[]):
    message = {
        sender_type + '_id': sender_id,
        'message': message_text
    }

    attachment_photos = []
    if len(message_photos) > 5:
        message_photos = message_photos[:5]
    for photo in message_photos:
        if photo[-3:] != 'gif':
            response = vk_upload.photo_messages(photo)[0]
            attachment_photos.append('photo{owner_id}_{id}'.format(
                owner_id=response['owner_id'],
                id=response['id']
            ))
        else:
            response = vk_upload.document(photo)[0]
            attachment_photos.append('doc{owner_id}_{id}'.format(
                owner_id=response['owner_id'],
                id=response['id']
            ))
    message['attachment'] = ','.join(attachment_photos)

    try:
        vk.method('messages.send', message)
    except vk_api.ApiError:
        sleep(1)
        message['message'] = 'Повторите Вашу команду, пожалуйста.'
        vk.method('messages.send', message)
    except vk_api.Captcha:
        print("VK adapter: captcha error")
        return False
    except ConnectionError:
        return False
    except vk_api.ApiHttpError:
        return False

    return True
