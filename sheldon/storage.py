# -*- coding: utf-8 -*-

"""
Interface to Redis-storage.

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""
from sheldon.utils import logger

# We will catch all import exceptions in bot.py
from redis import StrictRedis


class Storage:
    def __init__(self, bot):
        """
        Create new storage for bot

        :param bot: Bot object
        :return:
        """
        self.bot = bot

        # Connect to Redis.
        # If we had problems with Redis - just set self.redis to None.
        # Not redis-required modules must work without Redis.

        # We get parameters for redis connection from bot's config.
        self.redis = StrictRedis(
            host=bot.config.get('SHELDON_REDIS_HOST', 'localhost'),
            port=bot.config.get('SHELDON_REDIS_PORT', '6379'),
            db=bot.config.get('SHELDON_REDIS_DB', '0')
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
