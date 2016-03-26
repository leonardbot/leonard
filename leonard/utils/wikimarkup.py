# -*- coding: utf-8 -*-

"""
Parse wiki markup text to plain text. Designed for Wikihow.

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015
"""
import re
from leonard.utils import split_message

REF_TAG = '<ref>.+?</ref>'
DELETE_TAGS = ['{{fa}}', '{{reflist}}', '{{nointroimg}}', '__PARTS__', '<br>',
               '__Part__']
IMAGE_TAG_RE = '\[\[Image:.+?\]\]'
WHVID_RE = '\{\{whvid\|.+?\}\}'
STUB_RE = '\{\{Stub\|.+?\}\}'
CATEGORY_TAG_RE = '\[\[Category:.+?\]\]'
ARTICLE_LINK_RE = '\[\[.+?\|(.+?)\]\]'
WIKI_LINK_RE = '\[\[(.+?)\]\]'
HEADER_RE = '\n== ?(.+?) ?==\n'
SUBHEADER_RE = '\n=== ?(.+?) ?==='


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
    # Save only text from articles links
    markup = re.sub(ARTICLE_LINK_RE, lambda match: match.group(1), markup)
    # Delete other tags
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
                    lambda match: '&&&{}:\n\n'.format(match.group(1)),
                    markup)
    messages = markup.split('&&&')
    return messages


def parse_subheaders(markup):
    """
    Find and change subheaders in markup

    :param markup: str
    :return: str, new markup with changed subheaders
    """
    markup = re.sub(SUBHEADER_RE,
                    lambda match: '\n\n{}:'.format(match.group(1)),
                    markup)
    return markup


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
    # Delete ref tags
    markup = re.sub(REF_TAG, '', markup)
    # Delete whvid tags
    markup = re.sub(WHVID_RE, '', markup)
    # Delete stub tags
    markup = re.sub(STUB_RE, '', markup)
    # Delete square-brackets tags from markup
    markup = parse_square_brackets(markup)
    # Make Wikihow lists more beautiful
    markup = markup.replace('\n#', '\n*')
    # In Wikihow first paragraph is always short description of article.
    # So we can add it to description.
    messages.append(markup.split('\n')[0])
    # And delete it from original markup
    markup = '\n'.join(markup.split('\n')[1:])
    # Parse subheaders in messages
    markup = parse_subheaders(markup)
    # Small hack: if header is now first paragraph,
    # so imitate line ending to continue using regex for header.
    markup = '\n' + markup
    # Split markup by headers and save it to messages
    messages.extend(split_headers(markup))
    # Maybe messages is too big, so we should separate it by paragraphs
    # using split_message util
    new_messages = []
    for message in messages:
        new_messages.extend(split_message(message))
    messages = new_messages
    # Delete unusable line endings
    messages = list(map(lambda s: s.rstrip().lstrip(), messages))
    # Delete message only with '*'
    messages = list(filter(lambda x: x != '*', messages))
    # Delete empty messages
    messages = list(filter(None, messages))
    return messages
