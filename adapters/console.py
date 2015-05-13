from time import time
from os import getlogin

adapter_config = {
    "name": "console",
    "blocked_users_id": [],
    "admin_ids": [
        hash(getlogin())
    ]
}

def get_messages():
    message = input('Enter message:')
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
