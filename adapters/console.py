from time import time
from os import getlogin

console_adapter_config = {
    "name": "console",
    "enable": 1,
    "options": {}
}

def get_messages():
    message = input('Enter message:')
    return [{
        "message": message,
        "time": time(),
        "sender_id": None,
        "sender_name": getlogin(),
        "sender_type": None
    }]


def send_message(message_text="",
                 message_photos=[],
                 options={}):
    print("Text:", message_text)
    print("Photos:", message_photos)
    print("Options:", options)
