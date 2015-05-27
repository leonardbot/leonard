from time import sleep
from sheldon import Sheldon
import sys

bot = Sheldon(sys.argv[1], sys.argv[2])
bot.load_modules()
print('Bot loaded.')

while True:
    new_messages = bot.get_messages()
    for message in new_messages:
        if message['sender_id'] in bot.blocked_users:
            continue
        bot.parse_message(message)
    sleep(0.5)