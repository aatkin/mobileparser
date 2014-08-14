# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from parser_abc import Parser

__version__ = '0.1.0'


class Unica(Parser):
    def __init__(self):
        super(Unica, self).__init__("Unica", __version__)
