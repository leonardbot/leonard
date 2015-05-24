from sheldon import SheldonTest
from time import time

message = {
    "text": '!tj',
    "time": time(),
    "sender_id": 1,
    "sender_type": None,
    "user_id": 1
}
bot = SheldonTest('en')
bot.load_modules()

bad_command_message = 'Command is bad. Check it again.'


def test_module_in_loaded_modules():
    assert 'tj' in bot.loaded_modules


def test_getting_answer():
    bot.parse_message(message)
    assert 'Анализ СМИ:' in bot.sent_messages[-4]['message_text']
    assert 'Лучшие твиты:' in bot.sent_messages[-8]['message_text']
    assert 'Последние новости:' in bot.sent_messages[-12]['message_text']


def test_getting_answer_with_full_module_name():
    message['text'] = '!tjournal'
    bot.parse_message(message)
    assert 'Анализ СМИ:' in bot.sent_messages[-4]['message_text']
    assert 'Лучшие твиты:' in bot.sent_messages[-8]['message_text']
    assert 'Последние новости:' in bot.sent_messages[-12]['message_text']


def test_getting_answer_with_wrong_cmd():
    message['text'] = '!to'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message
