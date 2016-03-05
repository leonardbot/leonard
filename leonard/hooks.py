# -*- coding: utf-8 -*-

"""
Decorators and other functions for hooks.

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015
"""
import re
import threading

import ross as ross_module

from leonard.exceptions import catch_module_errors


class Hook:
    """
    Basic class for hooks
    """
    # Every hook has type. It could be
    # 'command' (command hook), 'message' (message hook),
    # 'interval' (interval hook), 'cron' (cron hook),
    # 'web' (web hook)
    type = ''
    func = None
    # Plugin object which hook from.
    plugin = None

    # If not one module return True after check,
    # bot sort matches by priority and choose first.
    priority = 0

    @catch_module_errors
    def call(self, incoming_message, bot):
        """
        Run hook

        :param incoming_message: Message object
        :param bot: Leonard object
        :return:
        """
        self.func.__call__(incoming_message, bot)


class MessageHook(Hook):
    def __init__(self, user_function, regexes,
                 case_sensitive=False, normalize=True):
        """
        Create new message hook

        :param user_function: decorated user's function, called
                              when regular expression matching with
                              incoming message
        :param regexes: regular expression for messages
        :param case_sensitive: bool, is hook catching messages
                                     with case sensitive
        :param normalize: bool, find words in normalized_message or not
        """
        self.type = 'message'
        self.priority = 4

        self.func = user_function

        if type(regexes) == str:
            regexes = [regexes]
        self.regexes = regexes

        self.case_sensitive = case_sensitive
        self.normalize = normalize

    def check(self, incoming_message):
        """
        Check, is this message catching for this hook

        :param incoming_message: IncomingMessage object
        :return: True or False
        """
        if self.normalize:
            message_text = incoming_message.normalizated_text
        else:
            message_text = incoming_message.text

        if not self.case_sensitive:
            for regex in self.regexes:
                match = re.match(regex, message_text, re.IGNORECASE)
                if match:
                    incoming_message.variables['regex_match'] = match.groups()
                    return True
        else:
            for regex in self.regexes:
                match = re.match(regex, message_text)
                if match:
                    incoming_message.variables['regex_match'] = match.groups()
                    return True

        return False


def message(regexes=[], case_sensitive=False, normalize=True):
    """
    Hook for catching messages, for example:
    "i want cat", "thanks" etc.

    :param regexes: list[string], regular expressions for catching messages
    :param case_sensitive: bool, is bot catching messages with case sensitive
    :param normalize: bool, find words in normalized_message or not
    :return:
    """

    def hook(func):
        def wrapped(message_object, bot_object):
            """
            Wrapper around user's function

            :param message_object: incoming message, Message object
            :param bot_object: Leonard object
            :return:
            """
            return func(message_object, bot_object)

        wrapped._leonard_hook = MessageHook(wrapped, regexes,
                                            case_sensitive, normalize)
        return wrapped

    return hook


class CommandHook(Hook):
    def __init__(self, user_function, command):
        """
        Create new command hook

        :param user_function: decorated user's function, called
                              when command matching with incoming message
        :param command: str, command text without '!'.
                        For example, 'join'.
        """
        self.type = 'command'
        self.priority = 1

        self.func = user_function
        self.command = command

    def check(self, incoming_message):
        """
        Check, is this message catching for this hook

        :param incoming_message: IncomingMessage object
        :return: True or False
        """
        return incoming_message.text.lstrip().startswith('!' + self.command)


def command(command_text):
    """
    Hook for catching commands, for example:
    "!asana", "!deploy leonard" etc.

    :param command_text: str, command text without '!'. For example, 'join'.
    :return:
    """

    def hook(func):
        def wrapped(message_object, bot_object):
            """
            Wrapper around user's function

            :param message_object: incoming message, Message object
            :param bot_object: Leonard object
            :return:
            """
            return func(message_object, bot_object)

        wrapped._leonard_hook = CommandHook(wrapped, command_text)
        return wrapped

    return hook


class CallbackHook(Hook):
    def __init__(self, user_function, callback_func):
        """
        Create new callback hook.

        :param user_function: decorated user's function, called
                              when callback matching with incoming message
        :param callback_func: func, that called with incoming_message and
                              it must return True or False
        """
        self.type = 'callback'
        self.priority = 1

        self.func = user_function
        self.callback_func = callback_func

    def check(self, incoming_message):
        """
        Check, is this message catching for this hook

        :param incoming_message: IncomingMessage object
        :return: True or False
        """
        return self.callback_func.__call__(incoming_message)


def callback(callback_func):
    """
    Hook for catching anything you want, based on
    your callback function

    :param callback_func: callback func, takes incoming message
                          and returns True or False
    :return:
    """

    def hook(func):
        def wrapped(message_object, bot_object):
            """
            Wrapper around user's function

            :param message_object: incoming message, Message object
            :param bot_object: Leonard object
            :return:
            """
            return func(message_object, bot_object)

        wrapped._leonard_hook = CallbackHook(wrapped, callback_func)
        return wrapped

    return hook


class KeywordsHook(Hook):
    def __init__(self, user_function, keywords_list, normalize=True):
        """
        Create new keywords hook.

        :param user_function: decorated user's function, called
                              when keywords matching with incoming message
        :param keywords_list: list of lists of str (keywords).
                              For example, [['weather', 'now'],
                                            ['weather', 'tomorrow']]
        :param normalize: bool, find words in normalized_message or not
        """
        self.type = 'keywords'
        self.priority = 3

        self.func = user_function
        self.keywords_list = keywords_list
        self.normalize = normalize

    def check(self, incoming_message):
        """
        Check, is this message catching for this hook

        :param incoming_message: IncomingMessage object
        :return: True or False
        """
        if self.normalize:
            message_text = incoming_message.normalizated_text
        else:
            message_text = incoming_message.text.lower()
        message_words = message_text.split()
        for keywords in self.keywords_list:
            # Create set for keywords to have ability to delete
            # keywords by words
            keywords_set = set(keywords)
            for word in keywords:
                if word.lower() in message_words:
                    keywords_set.remove(word)
            # If set is empty, so all words found, return True
            if keywords_set == set():
                return True
        return False


def keywords(keywords_list, normalize=True):
    """
    Hook for catching messages by keywords list.
    Hook match only when all words from one or more of keyword list
    (not list of keywords lists) is in the message words.

    :param keywords_list: list of lists of str (keywords).
                          For example, [['weather', 'now'],
                                        ['weather', 'tomorrow']]
    :param normalize: bool, find words in normalized_message or not
    :return:
    """

    def hook(func):
        def wrapped(message_object, bot_object):
            """
            Wrapper around user's function

            :param message_object: incoming message, Message object
            :param bot_object: Leonard object
            :return:
            """
            return func(message_object, bot_object)

        wrapped._leonard_hook = KeywordsHook(wrapped, keywords_list, normalize)
        return wrapped

    return hook


class StartEndHook(Hook):
    def __init__(self, user_function, words, normalize=True):
        """
        Create new start_end hook.

        :param user_function: decorated user's function, called
                              when callback matching with incoming message
        :param words: list of str, variants of start or end.
        :param normalize: bool, find words in normalized_message or not
        """
        self.type = 'start_end'
        self.priority = 2

        self.func = user_function
        self.words = words
        self.normalize = normalize

    def check(self, incoming_message):
        """
        Check, is this message catching for this hook

        :param incoming_message: IncomingMessage object
        :return: True or False
        """
        if self.normalize:
            message_text = incoming_message.normalizated_text
        else:
            message_text = incoming_message.text.lower()

        for word in self.words:
            if message_text.startswith(word) or message_text.endswith(word):
                query = message_text.replace(word, '')
                # Delete extra spaces
                query = ' '.join(query.split())
                incoming_message.variables['query'] = query
                return True
        return False


def start_end(starts_ends, normalize=True):
    """
    Hook for catching messages by defined starts or ends.
    For example, starts_ends=['book', 'booking'] will catch
    'book hotel', 'booking hotel', 'hotel book', 'hotel booking'.

    :param starts_ends: list of str, variants of starts and ends
    :param normalize: bool, find words in normalized_message or not
    :return:
    """

    def hook(func):
        def wrapped(message_object, bot_object):
            """
            Wrapper around user's function

            :param message_object: incoming message, Message object
            :param bot_object: Leonard object
            :return:
            """
            return func(message_object, bot_object)

        wrapped._leonard_hook = StartEndHook(wrapped, starts_ends, normalize)
        return wrapped

    return hook


class IntervalHook(Hook):
    def __init__(self, user_function, interval):
        """
        Create new interval hook.

        :param user_function: decorated user's function, called
                              when command matching with incoming message
        :param interval: schedule time from schedule module.
                         For example, schedule.every().wednesday.at("13:15").
        """
        self.type = 'interval'
        self.priority = 1

        self.func = user_function
        self.interval = interval

    @catch_module_errors
    def call(self, bot, incoming_message=None):
        """
        Call interval hook

        :param bot: Leonard object
        :param incoming_message: not using
        :return:
        """
        thread = threading.Thread(target=self.func, args=(bot, ))
        thread.start()


def interval(interval_object):
    """
    Hook for running code by intervals.
    All functionality needs to import from schedule module.

    :param interval_object: interval object from schedule module.
                            For example, schedule.every().wednesday.at("13:15")
    :return:
    """

    def hook(func):
        def wrapped(bot_object):
            """
            Wrapper around user's function

            :param bot_object: Leonard object
            :return:
            """
            return func(bot_object)

        wrapped._leonard_hook = IntervalHook(wrapped, interval_object)
        return wrapped

    return hook


class RossHook(Hook):
    def __init__(self, user_function, params):
        """
        Create new Ross hook.

        :param user_function: decorated user's function, called
                              when ross params matching with incoming message
        :param params: dict of Ross parameters for catching message.
                       {'type': 'note', 'subtype': 'add'}
        """
        self.type = 'ross'
        self.priority = 3

        self.func = user_function
        self.params = params

    def check(self, incoming_message):
        """
        Check, is this message catching for this hook

        :param incoming_message: IncomingMessage object
        :return: True or False
        """
        # Tip for refactoring:
        # Right now ross is working no so slow, but when it will,
        # try to get cached params from incoming_message.variables['ross']
        message_data = ross_module.process_message(
            incoming_message.uncleaned_text
        )
        if message_data is None:
            return False
        message_params = message_data.__dict__
        for (param_name, param_value) in self.params.items():
            if not (param_name in message_params
                and message_params[param_name] == param_value):
                return False

        # We should pass Ross data to plugin using message variables.
        incoming_message.variables['ross'] = message_params
        return True


def ross(**kwargs):
    """
    Hook for catching messages by defined Ross return params.
    Ross - library for parsing users' requests to bot.
    It's built specially for Leonard bot: https://github.com/leonardbot/ross
    For example, type='notes', subtype='add' will catch message that needed


    :param kwargs: dict of defined ross params. Hook catches message
                   if ALL params from hook contains (and equals, of course)
                   in message params.
    :return:
    """

    def hook(func):
        def wrapped(message_object, bot_object):
            """
            Wrapper around user's function

            :param message_object: incoming message, Message object
            :param bot_object: Leonard object
            :return:
            """
            return func(message_object, bot_object)

        wrapped._leonard_hook = RossHook(wrapped, kwargs)
        return wrapped

    return hook


def find_hooks(plugin):
    """
    Find hooks in plugin module

    :param plugin: Plugin object
    :return: list of list of Hook objects and list of IntervalHook objects
    """
    plugin_module = plugin.module
    hooks = []
    interval_hooks = []
    # Iterating throw plugin elements
    for name in plugin_module.__dict__.keys():
        item = plugin_module.__dict__[name]

        # Hooks are setting '_leonard_hook' parameters
        # on functions when they decorated.
        if hasattr(item, '_leonard_hook'):
            # Set plugin param of hook
            item._leonard_hook.plugin = plugin

        if (hasattr(item, '_leonard_hook') and
                    item._leonard_hook.type != 'interval'):
            hooks.append(item._leonard_hook)
        elif (hasattr(item, '_leonard_hook') and
                      item._leonard_hook.type == 'interval'):
            interval_hooks.append(item._leonard_hook)
    return [hooks, interval_hooks]
