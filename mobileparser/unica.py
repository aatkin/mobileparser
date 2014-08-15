# -*- coding: utf-8 -*-

__version__ = '0.1.4'

import logging
from bs4 import BeautifulSoup as bs
import requests
from parser_abc import Parser, Week, Day, Food

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
UNICA_RESTAURANTS = [UNICA_ASSARI, UNICA_BRYGGE, UNICA_DELICA,
                     UNICA_DELIPHARMA, UNICA_DENTAL, UNICA_MACCIAVELLI,
                     UNICA_MIKRO, UNICA_MYSSY, UNICA_NUTRITIO,
                     UNICA_RUOKAKELLO, UNICA_TOTTISALMI]


class Unica(Parser):
    # @abstractmethod
    def __init__(self):
        super(Unica, self).__init__("Unica", __version__)
        self.logger = logging.getLogger(" {0}".format(__name__))

    # @abstractmethod
    def parse_page(self, page):
        pass

    def parse_foods(self, html):
        return bs(html)

    def assert_foodlist_exist(self, soap):
        array = soap.select("#content .pad .menu-list")
        return (len(array) != 0)

    def encode_remove_eol(self, text):
        return text.encode('utf-8', 'ignore').strip().replace(
            '\n', '').replace('\t', '').replace('\r', '')

    def load_page(self, link):
        try:
            self.logger.info(" Loading page " + link)
            html = requests.get(link)
            return html

        except requests.ConnectionError, error:
            self.logger.error(
                """
                A network problem occurred while loading given URL {0}
                {1}
                """.format(str(link), str(error)))
            return 1

        except requests.Timeout, error:
            self.logger.error(
                """
                Request timed out while loading given URL {0}
                {1}
                """.format(str(link), str(error)))
            return 2

        except Exception, error:
            self.logger.exception(
                """
                Error happened while loading given URL {0}
                {1}
                """.format(str(link), str(error)))
            return 3
