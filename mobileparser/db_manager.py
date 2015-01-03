# -*- coding: utf-8 -*-

import logging
from pymongo import MongoClient


class DB_manager(object):

    def __init__(self):
        self.logger = logging.getLogger(" {0}".format(__name__))

    def init_db(self):
        self.client = MongoClient('localhost', 24730)
        self.db = self.client.mobileparser
        self.logger.debug('mongodb connection opened')

    def close_db(self):
        self.client.close()
        self.logger.debug('mongodb connection closed')

    def handle_data(self, data):
        self.logger.debug(data)
        for restaurant in data['restaurants']:
            serialized = self.todict(restaurant)
            self.logger.debug(serialized)
            self.update_restaurant(serialized, data)

    def update_restaurant(self, restaurant, data):
        self.db.restaurant.insert(restaurant)

    def todict(self, obj, classkey=None):
        if isinstance(obj, dict):
            data = {}
            for (k, v) in obj.items():
                data[k] = self.todict(v, classkey)
            return data
        elif hasattr(obj, "_ast"):
            return self.todict(obj._ast())
        elif hasattr(obj, "__iter__"):
            return [self.todict(v, classkey) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict(
                [(key, self.todict(value, classkey))
                 for key, value in obj.__dict__.iteritems()
                    if not callable(value) and not key.startswith('_')]
            )
            if classkey is not None and hasattr(obj, "__class__"):
                data[classkey] = obj.__class__.__name__
            return data
        else:
            return obj
