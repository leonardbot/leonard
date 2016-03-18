# -*- coding: utf-8 -*-

"""
Parse wiki markup text to plain text. Designed to use with Wikihow.

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015
"""
import re

DELETE_TAGS = ['{{fa}}', '{{reflist}}', '__PARTS__']
IMAGE_TAG_RE = '\[\[Image:.+?\]\]'
CATEGORY_TAG_RE = '\[\[Category:.+?\]\]'
WIKI_LINK_RE = '\[\[(.+?)\]\]'
HEADER_RE = '\n==(.+?)==\n'
SUBHEADER_RE = '\n===(.+?)==='


def parse_square_brackets(markup):
    """
    Parse and replace all '[[..]]' from markup
    :param markup: str, markup text
    :return: str, markup text without '[[..]]'
    """
    # Delete all image tags
    markup = re.sub(IMAGE_TAG_RE, '', markup)
    # Delete category tag
    markup = re.sub(CATEGORY_TAG_RE, '', markup)
    # Delete square brackets from other tags
    markup = re.sub(WIKI_LINK_RE, lambda match: match.group(1), markup)
    return markup


def split_headers(markup):
    """
    Split markup by headers (== HEADER ==), but save its' titles

    :param markup: str, markup text
    :return: list of str, messages list
    """
    # Header looks like '\n== Foo ==\n', lets change
    # it to '&&&Foo\n' and than split markup by '&&&'.
    # '&&&' - is just symbols that never contains in markup (i hope).
    markup = re.sub(HEADER_RE,
                    lambda match: '&&&{}\n\n'.format(match.group(1)),
                    markup)
    messages = markup.split('&&&')
    return messages


def parse_subheaders(messages):
    """
    Find and change subheaders in all messages

    :param messages: list of str
    :return: list of str, changed messages
    """
    new_messages = []
    for message in messages:
        message = re.sub(SUBHEADER_RE,
                         lambda match: '\n{}:'.format(match.group(1)),
                         message)
        new_messages.append(message)
    return new_messages


def parse_wikihow_markup(markup):
    """
    Parse Wikihow markup and split it into bot messages
    :param markup: str, markup text
    :return: list of str, bot messages
    """
    messages = []
    # First, delete all unneeded tags from markup
    for tag in DELETE_TAGS:
        markup = markup.replace(tag, '')
    # Delete square-brackets tags from markup
    markup = parse_square_brackets(markup)
    # In Wikihow first paragraph is always short description of article.
    # So we can add it to description.
    messages.append(markup.split('\n')[0])
    # And delete it from original markup
    markup = '\n'.join(markup.split('\n')[1:])
    # Split markup by headers and save it to messages
    messages.extend(split_headers(markup))
    # Split subheaders in messages
    messages = parse_subheaders(messages)
    # Delete empty messages
    messages = list(filter(None, messages))
    return messages
