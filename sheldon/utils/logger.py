# -*- coding: utf-8 -*-

"""
Functions for sending messages to log file

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""

import logging

# Set logging file
logging.basicConfig(filename='sheldon.log', level=logging.INFO)


def info_message(message):
    logging.info(message)


def warning_message(message):
    logging.warning(message)


def error_message(message):
    logging.error(message)


def critical_message(message):
    logging.critical(message)