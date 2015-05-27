from sheldon import SheldonTest
from time import time

message = {
    "text": '!site yandex.ru',
    "time": time(),
    "sender_id": 1,
    "sender_type": None,
    "user_id": 1
}
bot = SheldonTest('en')
bot.load_modules()

bad_command_message = 'Command is bad. Check it again.'


def test_module_in_loaded_modules():
    assert 'site' in bot.loaded_modules


def test_getting_answer_without_protocol():
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == "Site working"


def test_getting_answer_with_protocol():
    message['text'] = '!site http://yandex.ru'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == "Site working"


def test_getting_answer_with_not_working_site():
    message['text'] = '!site http://yandedsrsasfrex.ru'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == "Site not working"


def test_getting_answer_with_incorrect_site():
    message['text'] = '!site lulz'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == "Site not working"


def test_getting_answer_without_parameter():
    message['text'] = '!site'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message


def test_getting_answer_with_wrong_cmd():
    message['text'] = '!siet'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message
