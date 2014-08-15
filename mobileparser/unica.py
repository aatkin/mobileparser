# -*- coding: utf-8 -*-

__version__ = '0.1.3'

from bs4 import BeautifulSoup as bs
from parser_abc import Parser, Restaurant, Food

UNICA_BASE_URL = "http://www.unica.fi/fi/ravintolat/"
UNICA_ASSARI = {"name": "Assarin ullakko",
                "url": UNICA_BASE_URL + "assarin-ullakko/"}
UNICA_BRYGGE = {"name": "Brygge", "url": UNICA_BASE_URL + "brygge/"}
UNICA_DELICA = {"name": "Delica", "url": UNICA_BASE_URL + "delica/"}
UNICA_DELIPHARMA = {"name": "Delipharma",
                    "url": UNICA_BASE_URL + "deli-pharma/"}
UNICA_DENTAL = {"name": "Dental", "url": UNICA_BASE_URL + "dental/"}
UNICA_MACCIAVELLI = {"name": "Macciavelli",
                     "url": UNICA_BASE_URL + "macciavelli/"}
UNICA_MIKRO = {"name": "Mikro", "url": UNICA_BASE_URL + "mikro/"}
UNICA_MYSSY = {"name": "Myssy & Silinteri",
               "url": UNICA_BASE_URL + "myssy-silinteri/"}
UNICA_NUTRITIO = {"name": "Nutritio", "url": UNICA_BASE_URL + "nutritio/"}
UNICA_RUOKAKELLO = {"name": "Ruokakello",
                    "url": UNICA_BASE_URL + "ruokakello/"}
UNICA_TOTTISALMI = {"name": "Tottisalmi",
                    "url": UNICA_BASE_URL + "tottisalmi/"}


class Unica(Parser):
    def __init__(self, logger):
        super(Unica, self).__init__("Unica", __version__)
        self.logger = logger

    def parse_html(html):
        pass

    def load_page(link):
        try:
            LOG.info(" Loading page... " + link)
            page = url.urlopen(link).read()
            return page
        except url.URLError, e:
            LOG.exception(" Unable to connect to a given link: \n %s", str(e))
            return -1
