from sheldon import SheldonTest
from os import getlogin
from time import time

message = {
    "text": '!help',
    "time": time(),
    "sender_id": hash(getlogin()),
    "sender_type": None,
    "user_id": hash(getlogin())
}
bot = SheldonTest('en')
bot.load_modules()


def test_module_in_loaded_modules():
    assert 'help' in bot.loaded_modules


def test_getting_answer():
    bot.parse_message(message)
    for module in bot.loaded_modules:
        assert module in bot.sent_messages[-1]['message_text']


def test_getting_answer_with_wrong_cmd():
    message['text'] = '!halp'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == "Command is bad. Check it again."
