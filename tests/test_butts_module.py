from sheldon import SheldonTest
from time import time

message = {
    "text": '!butts',
    "time": time(),
    "sender_id": 1,
    "sender_type": None,
    "user_id": 1
}
bot = SheldonTest('en')
bot.load_modules()

bad_command_message = 'Command is bad. Check it again.'


def test_module_in_loaded_modules():
    assert 'butts' in bot.loaded_modules


def test_getting_answer():
    bot.parse_message(message)
    assert len(bot.sent_messages[-1]['message_photos']) == 1


def test_getting_answer_with_wrong_cmd():
    message['text'] = '!batts'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message
