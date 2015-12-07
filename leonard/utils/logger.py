# -*- coding: utf-8 -*-

"""
Functions for sending messages to log file

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""

import sys
import logging

# Setup logging
log = logging.getLogger()
log.setLevel(logging.INFO)
log_stream = logging.StreamHandler(sys.stdout)
log_stream.setLevel(logging.WARNING)
log.addHandler(log_stream)


def info_message(message):
    log.info(message)


def warning_message(message):
    log.warning(message)


def error_message(message):
    log.error(message)


def critical_message(message):
    log.critical(message)