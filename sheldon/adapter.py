# -*- coding: utf-8 -*-

"""
Functions and classes for adapter working

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""

import importlib

from sheldon.utils import logger
from sheldon.config import parse_config


class Adapter:
    """
    Adapter class contains information about adapter:
    name, variables and module using to call adapter methods.
    All adapters inherited from Adapter class'
    """

    def __init__(self, name, module, config):
        """
        Init new Adapter object

        :param name: public name of adapter which used in
                     config/adapters directory
        :param module: imported adapter's module
        :param config: ModuleConfig, parsed adapter config
        """
        self.name = name
        self.module = module
        self.config = config


class Message:
    """
    Class for every message: incoming and outgoing.
    """
    def __init__(self, text='', attachments=[], channel=None, variables={}):
        """
        Create new message.

        :param text: string, text of message
        :param attachments: list[Attachment] or Attachment object,
                                    attachments with message
        :param channel: Message's channel: channel in Slack, room in Hipchat etc.
        :param variables: dict, external parameters from/to adapter:
                          may be 'slack_username', 'slack_emoji', 'telegram_id'
                          Read about those in adapters' documentation.
                          Parameters should start from adapter name.
        """
        self.text = text
        # If attachment only one, convert it to list
        if type(attachments) == Attachment:
            self.attachments = [attachments]
        else:
            self.attachments = attachments
        self.channel = channel
        self.variables = variables


class IncomingMessage(Message):
    """
    Class for messages from user.
    """

    def __init__(self, sender, *args, **kwargs):
        """
        Create new message from user.

        :param sender: User object, sender of message
        """
        super().__init__(*args, **kwargs)
        self.sender = sender


class OutgoingMessage(Message):
    """
    Class for messages from bot.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Attachment:
    """
    Class for every attachment: incoming and outgoing
    """

    def __init__(self, attachment_type, attachment_path=None,
                 attachment_text='', attachment_id=None):
        """
        Init new attachment.

        :param attachment_type: 'photo', 'video', 'link'
                                and other things, supported by adapter
        :param attachment_path: path to photo, video, url etc.
        :param attachment_text: optional text of attachment - may
                                be сaption or something another
        :param attachment_id: int, not required id of attachment from adapter
        :return:
        """
        self.type = attachment_type.lower()
        self.path = attachment_path
        self.text = attachment_text
        self.id = attachment_id


def load_adapter(adapter_name):
    """
    Load adapter which set in bot config.

    :param adapter_name: name of adapter. May be local package in
                         adapters folder or package from PyPi.
    :return:
    """
    # Try to import adapter from project directory
    adapter_module = import_adapter('adapters.{}'.format(adapter_name))

    # If it failed, try to import it as PyPi module
    if adapter_module is None:
        adapter_module = import_adapter(adapter_name)

    # If it still fail, just return error
    if adapter_module is None:
        logger.critical_message('Problems with importing adapter')
        return None

    adapter_config = parse_config(adapter_module)

    adapter_object = Adapter(adapter_name,
                             adapter_module,
                             adapter_config)
    return adapter_object


def import_adapter(package_name):
    """
    Import adapter using importlib

    :param package_name: full name of adapter, ex. 'adapters.console'
    :return:
    """
    try:
        return importlib.import_module(package_name)
    except ImportError as error:
        logger.critical_message(error)
        return None
