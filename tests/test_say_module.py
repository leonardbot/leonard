from sheldon import SheldonTest
from time import time

message = {
    "text": '!say something',
    "time": time(),
    "sender_id": 1,
    "sender_type": None,
    "user_id": 1
}
bot = SheldonTest('en')
bot.load_modules()

bad_command_message = 'Command is bad. Check it again.'


def test_module_in_loaded_modules():
    assert 'say' in bot.loaded_modules


def test_getting_answer():
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == "something"


def test_getting_answer_without_parameter():
    message['text'] = '!say'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message


def test_getting_answer_with_wrong_cmd():
    message['text'] = '!sayd something'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message
