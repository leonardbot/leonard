# -*- coding: utf-8 -*-

"""
Functions for sending messages to stdout or log file

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""


def info_message(*args):
    print('INFO: ', *args, end='\n\n')


def warning_message(*args):
    print('WARNING: ', *args, end='\n\n')


def error_message(*args):
    print('ERROR: ', *args, end='\n\n')


def critical_message(*args):
    print('CRITICAL ERROR: ', *args, end='\n\n')
