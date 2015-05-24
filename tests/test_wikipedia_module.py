from sheldon import SheldonTest
from time import time

message = {
    "text": '!wiki Steve Jobs',
    "time": time(),
    "sender_id": 1,
    "sender_type": None,
    "user_id": 1
}
bot = SheldonTest('en')
bot.load_modules()

bad_command_message = 'Command is bad. Check it again.'


def test_module_in_loaded_modules():
    assert 'wikipedia' in bot.loaded_modules


def test_getting_answer_with_people():
    bot.parse_message(message)
    assert 'Steven Paul "Steve" Jobs' in bot.sent_messages[-1]['message_text']


def test_getting_answer_with_animal():
    message['text'] = '!wiki cat'
    bot.parse_message(message)
    assert 'cat' in bot.sent_messages[-1]['message_text']


def test_getting_answer_with_full_name_of_module():
    message['text'] = '!wikipedia cat'
    bot.parse_message(message)
    assert 'cat' in bot.sent_messages[-1]['message_text']


def test_getting_answer_with_movie():
    message['text'] = '!wiki Fast And Furious'
    bot.parse_message(message)
    assert 'The Fast and the Furious' in bot.sent_messages[-1]['message_text']


def test_getting_answer_with_incorrect_param():
    message['text'] = '!wiki Fhfdkvsfncdnsdvjn'
    bot.parse_message(message)
    assert "I don't know" == bot.sent_messages[-1]['message_text']


def test_getting_answer_without_parameter():
    message['text'] = '!wiki'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message


def test_getting_answer_with_wrong_cmd():
    message['text'] = '!sayd something'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message
