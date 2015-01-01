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
        self.logger.info(data)
