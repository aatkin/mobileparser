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
        parser_info = {
            "parser_version": data["parser_version"],
            "parser_name": data["parser_name"].lower(),
            "parse_date": data["parse_date"]
        }
        for restaurant in data['restaurants']:
            serialized = self.todict(restaurant)
            serialized["parser_info"] = parser_info
            self.logger.debug(serialized)
            self.update_restaurant(serialized)

    def update_restaurant(self, restaurant):
        name = restaurant["restaurant_info"]["name"]
        week = restaurant["foodlist_date"]["week_number"]
        year = restaurant["foodlist_date"]["year"]
        searched = {
            "restaurant_info.name": name,
            "foodlist_date.week_number": week,
            "foodlist_date.year": year
        }
        self.db.restaurant.update(searched, restaurant, upsert=True)

    def update_parser_version(self, version):
        self.db.info.save({"version": version})

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
