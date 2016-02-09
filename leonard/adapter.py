# -*- coding: utf-8 -*-

"""
Functions and classes for adapter working

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015
"""

import importlib

from leonard.utils import logger
from leonard.config import parse_config


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
    def __init__(self, text='', attachments=[], variables={}):
        """
        Create new message.

        :param text: string, text of message
        :param attachments: list[Attachment] or Attachment object,
                                    attachments with message
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
        self.variables = variables
        # Correct locale for hooked plugin.
        # For example, object of EnglishLocale of hello plugin
        self.locale = None

    def __str__(self):
        # If message.text length is more than 15 chars, trim it
        if len(self.text) > 15:
            message_preview = self.text[:15] + '...'
        else:
            message_preview = self.text
        answer = 'Message "{}", variables: {}'.format(
            message_preview, self.variables
        )
        if type(self) == IncomingMessage:
            answer += ' from {}'.format(self.sender)
        else:
            answer += ' to {}'.format(self.recipient)
        return answer


class IncomingMessage(Message):
    """
    Class for messages from user.
    """

    def __init__(self, adapter_id, *args, **kwargs):
        """
        Create new message from user.

        :param adapter_id: str, message sender id from adapter.
                           For example, 'console12983'
        """
        super().__init__(*args, **kwargs)
        self.adapter_id = adapter_id
        # Sender will be set by users middleware
        self.sender = None


class OutgoingMessage(Message):
    """
    Class for messages from bot.
    """

    def __init__(self, recipient, *args, **kwargs):
        """
        Create new message from bot

        :param recipient: User object
        :return:
        """
        super().__init__(*args, **kwargs)
        self.recipient = recipient


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

    adapter_config = parse_config(adapter_module, 'adapter')

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
        logger.error_message(error)
        return None
