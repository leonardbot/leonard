# -*- coding: utf-8 -*-

"""
Interface to MongoDB storage.

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""
from leonard.utils import logger

from pymongo import MongoClient
from bson import ObjectId


class Database:
    """
    Class for MongoDB client to store users data
    """
    def __init__(self, bot, config_prefix):
        """
        Create new db for storing users information

        :param bot: Leonard object
        :param config_prefix: prefix of variables in config. Default - 'LEONARD_'
        :return:
        """
        self.client = MongoClient(bot.config.get(
            '{}MONGODB_URI'.format(config_prefix),
            'mongodb://localhost:27017'
        ))
        self.db = self.client.leonard
        self.collection = self.db.users

    def find_by_adapter_id(self, adapter_id):
        """
        Find user by id string

        :param adapter_id: str, user id from adapter
        :return: User object
        """
        cursor = self.collection.find({
            'adapter_id': adapter_id
        })
        if cursor.count() == 0:
            return self.create_new_user(adapter_id)

        user = list(cursor)[0]
        return User(user['adapter_id'], user)

    def create_new_user(self, adapter_id):
        """
        Create new user in MongoDB

        :param adapter_id: str, user id from adapter
        :return: User object
        """
        result = self.collection.insert_one({
            'adapter_id': adapter_id
        })
        user = list(
            self.collection.find({
                '_id': ObjectId(result.inserted_id)
            })
        )[0]
        return User(user['adapter_id'], user)


class User:
    """
    Class for each user to store his data
    """
    def __init__(self, adapter_id, data):
        """
        Create new user object from user in MongoDB

        :param adapter_id: str, user id from adapter
        :param data: dict with user data from database
        :return:
        """
        self.adapter_id = adapter_id
        self.data = data
