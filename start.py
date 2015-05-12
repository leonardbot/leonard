from time import sleep
from sheldon import Sheldon
from settings import bot_language, bot_adapter

bot = Sheldon(bot_language, bot_adapter)
bot.load_modules()

while True:
    new_messages = bot.get_messages()
    for message in new_messages:
        bot.parse_message(message)
    sleep(0.5)