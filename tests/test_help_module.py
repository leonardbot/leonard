from sheldon import SheldonTest
from time import time

message = {
    "text": '!help',
    "time": time(),
    "sender_id": 1,
    "sender_type": None,
    "user_id": 1
}
bot = SheldonTest('en')
bot.load_modules()


def test_module_in_loaded_modules():
    assert 'help' in bot.loaded_modules


def test_getting_answer():
    bot.parse_message(message)
    for module_num in range(1, len(bot.loaded_modules) + 1):
        assert bot.sent_messages[-module_num]['message_text']


def test_getting_answer_with_wrong_cmd():
    message['text'] = '!halp'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == "Command is bad. Check it again."
