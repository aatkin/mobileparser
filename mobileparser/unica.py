# -*- coding: utf-8 -*-

__version__ = '0.1.0'

from bs4 import BeautifulSoup as bs
from parser_abc import Parser, Restaurant, Food


class Unica(Parser):
    def __init__(self):
        super(Unica, self).__init__("Unica", __version__)

    def parse_html(html):
        pass
