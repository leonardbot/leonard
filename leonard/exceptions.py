# -*- coding: utf-8 -*-

"""
Tools for catching exceptions

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015
"""

import os
import bugsnag
from leonard.utils import logger, NextHook

bugsnag.configure(
  api_key=os.environ['LEONARD_BUGSNAG_KEY'],
  project_root=os.getcwd(),
  release_stage=os.environ.get('ENV', 'development')
)


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
            bugsnag.notify(error)

            if type(error) == NextHook:
                raise NextPluginHook

    return wrapper
