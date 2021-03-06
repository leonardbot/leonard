# -*- coding: utf-8 -*-

"""
Interface to Redis-storage.

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (C) 2015
"""

import json

from redis import StrictRedis

from leonard.utils import logger


class Storage:
    def __init__(self, bot, config_prefix):
        """
        Create new storage for bot

        :param bot: Leonard object
        :param config_prefix: prefix of variables in config. Default - 'LEONARD_'
        :return:
        """

        # Connect to Redis.
        # If we had problems with Redis - just set self.redis to None.
        # Not redis-required modules must work without Redis.

        # We get parameters for redis connection from bot's config.
        self.redis = StrictRedis(
            host=bot.config.get('{}REDIS_HOST'.format(config_prefix), 'localhost'),
            port=bot.config.get('{}REDIS_PORT'.format(config_prefix), '6379'),
            db=bot.config.get('{}REDIS_DB'.format(config_prefix), '0')
        )
        try:
            # Check Redis connection
            self.redis.client_list()
        except Exception as error:
            logger.error_message('Error while connecting Redis:')
            logger.error_message(str(error))
            self.redis = None

    def get(self, key, default_value=None):
        """
        Get value from redis storage

        :param key: string, redis key for needed value
        :param default_value: string, value that returns if
                              key not found or redis isn't
                              connected to this bot
        :return: value with that key or default value
        """
        # If we had problems with redis connection,
        # return None or other default value
        if not self.redis:
            logger.warning_message("Redis not available for {} key".format(
                key
            ))
            return default_value

        value = self.redis.get(key)
        if value is not None:
            return value
        else:
            return default_value

    def set(self, key, value):
        """
        Set key to value in redis storage

        :param key: string
        :param value: string
        :return:
        """
        if not self.redis:
            logger.warning_message("{} key didn't save in storage".format(
                key
            ))
            return None

        return self.redis.set(key, value)

    def get_json(self, key, default_value=None):
        """
        Get value from Redis and parse JSON in it

        :param key: str
        :param default_value: string, value that returns if
                              key not found or redis isn't
                              connected to this bot
        :return: list/dict
        """
        value = self.get(key, default_value)
        if not value:
            return value
        if type(value) not in [list, dict]:
            return json.loads(value.decode('utf-8'))
        return value

    def set_json(self, key, value):
        """
        Dump value into json and save it in Redis

        :param key: string
        :param value: list/dict
        :return:
        """
        json_value = json.dumps(value)
        return self.set(key, json_value)
