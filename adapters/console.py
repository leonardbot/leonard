from time import time

i = 0

adapter_config = {
    "name": "console",
    "blocked_users_id": [],
    "admin_ids": [
        1
    ]
}


def get_messages():
    message = input('Enter message:')
    return [{
        "text": message,
        "time": time(),
        "sender_id": 1,
        "sender_type": None,
        "user_id": 1
    }]


def send_message(sender_id, sender_type,
                 message_text="", message_photos=[]):
    print("Text:", message_text)
    print("Photos:", message_photos)
    return True
