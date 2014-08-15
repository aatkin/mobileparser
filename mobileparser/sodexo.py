# -*- coding: utf-8 -*-

__version__ = '0.1.0'

from bs4 import BeautifulSoup as bs
from parser_abc import Parser, Restaurant, Food


class Sodexo(Parser):
    def __init__(self, logger):
        super(Sodexo, self).__init__("Sodexo", __version__)
        self.logger = logger

    def parse_html(html):
        pass
