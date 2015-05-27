from pytg import Telegram
from pytg.utils import coroutine
import os

adapter_config = {
    "name": "telegram",
    "blocked_users_id": [],
    "admin_ids": [
        "user#23897509"
    ]
}

telegram_connect = Telegram(
    telegram=os.environ['TG_PATH'] + 'bin/telegram-cli',
    pubkey_file=os.environ['TG_PATH'] + 'tg-server.pub'
)
telegram_sender = telegram_connect.sender
telegram_receiver = telegram_connect.receiver
message = {}


@coroutine
def parse_telegram_messages():
    global message
    msg = (yield)
    # If message was sent by bot,
    # return []
    if msg['own']:
        message = []
        return False
    if 'text' not in msg:
        msg['text'] = ''
    message = {
        'text': msg['text'],
        'time': msg['date'],
        'sender_id': msg['sender']['cmd'],
        'sender_type': msg['sender']['type'],
        'user_id': msg['sender']['cmd']
    }
    if msg['receiver']['type'] == 'chat':
        message['sender_id'] = msg['receiver']['cmd']
        message['sender_type'] = 'chat'
    message = [message]
    return True


def get_messages():
    global message
    telegram_receiver.start()
    try:
        telegram_receiver.message(
            parse_telegram_messages()
        )
    except KeyboardInterrupt:
        telegram_receiver.stop()
        exit()
    return message


def send_message(sender_id, sender_type,
                 message_text="", message_photos=[]):
    telegram_sender.send_msg(sender_id, message_text)
    for photo in message_photos:
        if photo[-3:] == 'gif':
            telegram_sender.send_document(sender_id, os.path.abspath(photo))
        else:
            telegram_sender.send_photo(sender_id, os.path.abspath(photo))
    return True
