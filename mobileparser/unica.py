# -*- coding: utf-8 -*-

__version__ = '0.2.0'

import logging
import requests
import lxml
import re
from bs4 import BeautifulSoup as bs
from parser_abc import Parser, Restaurant, Day, Food

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
    def parse(self):
        pass

    # @abstractmethod
    def parse_page(self, link):
        pass

    def parse_foods(self, soup):
        weekly_foods = {}
        week_days = soup.select("#content .menu-list .accord")
        for index, day in enumerate(week_days):
            try:
                day_name = self.encode_remove_eol(day.h4.getText())
                day_number = index

                lunch_elements = day.table.select(".lunch")
                diet_elements = day.table.select(".limitations")
                price_elements = day.table.select(".price")
                try:
                    alert_element = self.encode_remove_eol(day.table.find(
                        "span", {"class": "alert"}).getText())
                except Exception, e:
                    alert_element = ""

                daily_lunches = [self.encode_remove_eol(x.getText())
                                 for x in lunch_elements]
                daily_diets = [self.encode_remove_eol(x.getText())
                               for x in diet_elements]
                daily_prices = [re.findall(r"\d\,\d\d", self.encode_remove_eol(
                    x.getText())) for x in price_elements]
                daily_foods = [Food(name, diets, prices)
                               for name, diets, prices in zip(daily_lunches,
                                                              daily_diets,
                                                              daily_prices)]
                weekly_foods[day_number] = Day(
                    day_name, day_number, daily_foods, alert_element)
            except Exception, e:
                self.logger.exception(e)

        return weekly_foods

    def parse_opening_times(self, soup):
        print "todo"
        pass

    def parse_restaurant_info(self, soup):
        pass

    def assert_foodlist_exist(self, soup):
        menu_list = soup.select("#content .pad .menu-list")
        lunches = soup.select("#content .pad .menu-list .lunch")
        menu_isnt_empty = len(menu_list) != 0
        lunches_arent_empty = len(lunches) != 0
        return (menu_isnt_empty and lunches_arent_empty)

    def encode_remove_eol(self, text):
        try:
            return text.encode('utf-8', 'ignore').strip().replace(
                '\n', '').replace('\t', '').replace('\r', '')
        except UnicodeEncodeError, e:
            self.logger.exception(e)
            return text

    def load_page(self, link):
        try:
            self.logger.info(" Loading page " + link)
            html = requests.get(link)
            return html
        except Exception, e:
            raise Exception(e)

    def __repr__(self):
        return "{0} version {1}".format(self.name, __version__)
