# -*- coding: utf-8 -*-

"""
@author: Kirill Python
@contact: https://vk.com/python273
"""

import vk_api
import os

LOGFORMAT = """
REQUEST:
URL: {} {}
PARAMS: {}

RESPONSE:
CODE: {}
COOKIES: {}
TEXT:\n
{}
\n
"""


class ReqLogger:
    def __init__(self, session):
        self.session = session

        self.logfile = open('reqlog.txt', 'w', encoding='utf-8')

    def __call__(self, r, *args, **kwargs):
        print('Response url:', r.url)

        self.logfile.write(LOGFORMAT.format(
            r.request.url, r.request.method, r.request.body,
            r.status_code, self.session.cookies, r.text
        ))

    def close(self):
        self.logfile.close()


def main():
    """ Пример получения последнего сообщения со стены """
    print('Log may contain authorization data')

    login, password = os.environ['VK_LOGIN'], os.environ['VK_PASSWORD']
    vk = vk_api.VkApi(login, password)

    reqlogger = ReqLogger(vk.http)

    vk.http.hooks = {
        'response': reqlogger
    }

    try:
        vk.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)

    reqlogger.close()

if __name__ == '__main__':
    main()