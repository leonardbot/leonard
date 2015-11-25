# -*- coding: utf-8 -*-

"""
Tools for catching exceptions

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""

from sheldon.utils import logger


def catch_module_errors(module_call_function):
    """
    Catch all module exceptions and log it

    :param module_call_function: function with calling user module
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            module_call_function(*args, **kwargs)
        except Exception as error:
            error_message = str(error)
            logger.error_message('Module error: \n' + error_message)

    return wrapper
