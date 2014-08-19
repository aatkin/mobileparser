# -*- coding: utf-8 -*-

__version__ = '0.2.0'

import logging
import requests
import lxml
import re
from bs4 import BeautifulSoup as bs
from parser_abc import Parser, Restaurant, Day, Food
from restaurant_urls import UNICA_RESTAURANTS as unica_urls


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
                except AttributeError, e:
                    # alert element not found, assign empty string
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

    def parse_restaurant_info(self, soup, name, url):
        restaurant_elements = soup.select(
            "div#maplist ul.append-bottom li.color")
        try:
            for restaurant in restaurant_elements:
                restaurant_url = self.encode_remove_eol(
                    restaurant.attrs['data-uri'])
                if restaurant_url not in url:
                    pass
                else:
                    address = self.encode_remove_eol(
                        restaurant.attrs['data-address'])
                    zip_code = self.encode_remove_eol(
                        restaurant.attrs['data-zip'])
                    post_office = self.encode_remove_eol(
                        restaurant.attrs['data-city'])
                    longitude = self.encode_remove_eol(
                        restaurant.attrs['data-longitude'])
                    latitude = self.encode_remove_eol(
                        restaurant.attrs['data-latitude'])
                    restaurant_info = {
                        "name": name,
                        "address": address,
                        "zip_code": zip_code,
                        "post_office": post_office,
                        "longitude": longitude,
                        "latitude": latitude
                    }
                    return restaurant_info
        except Exception, e:
            self.logger.exception(e)

    def parse_week_number(self, soup):
        try:
            head_element = soup.select(
                "#content .pad .head2")[0].getText().encode("utf-8", "ignore")
            week_number = int(re.findall(r"\d\d", head_element)[0])
            return week_number
        except Exception, e:
            self.logger.exception(e)

    def assert_foodlist_exists(self, soup):
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
