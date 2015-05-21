from sheldon import SheldonTest
from time import time

message = {
    "text": '!module delete test',
    "time": time(),
    "sender_id": 1,
    "sender_type": None,
    "user_id": 1
}
bot = SheldonTest('en')
bot.load_modules()

incorrect_module_message = "Module doesn't exists. Check it again."
bad_command_message = 'Command is bad. Check it again.'
not_admin_message = 'You are not admin.'
test_complete_message = "Test completed. Message: '!test'"

def test_module_in_loaded_modules():
    assert 'modules' in bot.loaded_modules


def test_deleting_without_admin():
    message['user_id'] = -1
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == not_admin_message


def test_deleting_incorrect_module():
    message['user_id'] = 1
    message['text'] = '!module delete foobar'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == incorrect_module_message


def test_deleting_module():
    message['text'] = '!module delete test'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == 'Deleted.'


def test_deleted_module():
    message['text'] = '!test'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == bad_command_message


def test_adding_without_admin():
    message['user_id'] = -1
    message['text'] = '!module add test'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == not_admin_message


def test_adding_incorrect_module():
    message['user_id'] = 1
    message['text'] = '!module add foobar'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == incorrect_module_message


def test_adding_module():
    message['text'] = '!module add test'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == 'Added.'


def test_added_module():
    message['text'] = '!test'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == test_complete_message


def test_getting_answer_with_wrong_cmd():
    message['text'] = '!modzle'
    bot.parse_message(message)
    assert bot.sent_messages[-1]['message_text'] == "Command is bad. Check it again."
