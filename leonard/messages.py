# -*- coding: utf-8 -*-

"""
Functions for getting localized messages text

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""

import os
import yaml

messages = {}
messages_files = os.listdir('messages')
for file_name in messages_files:
    # If it not YAML document, continue to next file
    if not file_name.endswith('yml'):
        continue

    with open('messages/' + file_name) as file:
        # Delete file extesion for accessing messages
        # only by name
        messages[file_name.strip('.yml')] = yaml.load(file.read())


def get_text(name, incoming_message=None):
    """
    Get data for message in incoming message language
    from plugin file messages folder

    :param name: str, message name.
                 Format: '<module_name>.<path in module commands config
                                         separated by dot>'
                 For example, 'hello.hello_message',
                              'hello.bye_messages.aggressive'
    :param incoming_message: IncomingMessage object, needed for determine
                             user's language
    :return: str (message text), list of str (list of text)
    """
    # Split name of text message by dot
    # to find needed message in messages dictionary
    name_path = name.split('.')
    # First, out result is full messages dict
    result = messages
    # Iterating throw the parts of name path
    for name_part in name_path:
        # New result is result for name part
        try:
            result = result[name_part]
        except (TypeError, KeyError):
            return None
    # Choose right message for user language.
    # If result is dict, it should be dict with
    # different language versions of message.
    if type(result) == dict:
        try:
            return result[incoming_message.sender.language]
        except (TypeError, KeyError):
            return None
    return result
