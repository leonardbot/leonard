from time import time
from os import getlogin

console_adapter_config = {
    "name": "console",
    "options": {},
    "blocked_users_id": [],
    "bot_admins_id": [
        hash(getlogin())
    ]
}

def get_messages():
    message = input('Enter message:')
    return [{
        "message": message,
        "time": time(),
        "sender_id": hash(getlogin()),
        "sender_name": getlogin(),
        "sender_type": None,
        "options": {}
    }]


def send_message(message_text="",
                 message_photos=[],
                 options={}):
    print("Text:", message_text)
    print("Photos:", message_photos)
    print("Options:", options)
