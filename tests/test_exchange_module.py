from sheldon import SheldonTest
from time import time

message = {
    "text": '!to dollars 5 euro',
    "time": time(),
    "sender_id": 1,
    "sender_type": None,
    "user_id": 1
}
bot = SheldonTest('en')
bot.load_modules()

bad_command_message = 'Command is bad. Check it again.'
incorrect_number_message = 'Enter correct number.'
incorrect_currency_message = 'Enter correct currency.'


def test_module_in_loaded_modules():
    assert 'exchange' in bot.loaded_modules


def test_getting_answer_from_euro_to_dollars():
    bot.parse_message(message)
    assert '5 EUR - ' in bot.sent_messages[-1]['message_text']
    assert 'USD' in bot.sent_messages[-1]['message_text']


def test_getting_answer_from_dollars_to_euro():
    message['text'] = '!euro 1 dollar'
    bot.parse_message(message)
    assert '1 USD - ' in bot.sent_messages[-1]['message_text']
    assert 'EUR' in bot.sent_messages[-1]['message_text']


def test_getting_answer_from_dollars_to_rubles():
    message['text'] = '!to rubles 15 dollars'
    bot.parse_message(message)
    assert '15 USD - ' in bot.sent_messages[-1]['message_text']
    assert 'RUB' in bot.sent_messages[-1]['message_text']


def test_getting_answer_from_rubles_to_euro():
    message['text'] = '!to euro 1 ruble'
    bot.parse_message(message)
    assert '1 RUB - ' in bot.sent_messages[-1]['message_text']
    assert 'EUR' in bot.sent_messages[-1]['message_text']


def test_incorrect_number():
    message['text'] = '!to euro dsk rubles'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message


def test_negative_number():
    message['text'] = '!to euro -50 rubles'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message


def test_incorrect_first_currency():
    message['text'] = '!to pollars 5 rubles'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message


def test_incorrect_second_currency():
    message['text'] = '!to dollars 5 rublz'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message


def test_getting_dollars_rate_without_parameter():
    message['text'] = '!dollar'
    bot.parse_message(message)
    # Before space in message - current rate,
    # after - currency
    assert bot.sent_messages[-1]['message_text'].split(' ')[1] == 'EUR'


def test_getting_euro_rate_without_parameter():
    message['text'] = '!euro'
    bot.parse_message(message)
    # Before space in message - current rate,
    # after - currency
    assert bot.sent_messages[-1]['message_text'].split(' ')[1] == 'USD'


def test_getting_rubles_rate_without_parameter():
    message['text'] = '!ruble'
    bot.parse_message(message)
    # Before space in message - current rate,
    # after - currency
    assert bot.sent_messages[-1]['message_text'].split(' ')[1] == 'USD'


def test_getting_answer_with_wrong_cmd():
    message['text'] = '!to dollarz 5 rubles'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message
