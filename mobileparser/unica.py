# -*- coding: utf-8 -*-

__version__ = '0.4.0'

import logging
import requests
import lxml
import re
import datetime
from bs4 import BeautifulSoup as bs

from parser_exceptions import *
from parser_abc import Parser, Restaurant, Day, Food
from restaurant_urls import UNICA_RESTAURANTS as unica_urls


class Unica(Parser):
    # @abstractmethod
    def __init__(self):
        super(Unica, self).__init__("Unica", __version__)
        self.logger = logging.getLogger(" {0}".format(__name__))

    # @abstractmethod
    def parse(self):
        parse_results = []
        for url in unica_urls:
            page = self.load_page(url["url_fi"])
            soup = bs(page.text, "lxml")
            restaurant, error = self.parse_page(soup, url["url_fi"])
            if error:
                self.logger.debug("Restaurant foods were not found")
            parse_results.append(restaurant)
        parse_date = str(datetime.date.today())
        return {
            "restaurants": parse_results,
            "parser_version": self.version,
            "parser_name": self.name,
            "parse_date": parse_date
        }

    # @abstractmethod
    def parse_page(self, soup, link):
        if self.assert_foodlist_exists(soup):
            week_number = self.parse_week_number(soup)
            weekly_foods = self.parse_foods(soup)
            restaurant_info = self.parse_restaurant_info(soup, link)
            restaurant = Restaurant(restaurant_info,
                                    weekly_foods,
                                    week_number)
            return restaurant, False
        else:
            week_number = datetime.date.today().isocalendar()[1]
            restaurant_info = self.parse_restaurant_info(soup, link)
            restaurant = Restaurant(restaurant_info,
                                    "",
                                    week_number)
            return restaurant, True

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
        # contains opening hours
        opening_hours_elements = soup.select("#content .pad.mod .threecol")
        if len.opening_hours_elements == 0:
            raise Exception('No opening hours found!')

        weekdays = ['ma', 'ti', 'ke', 'to', 'pe', 'la']

        if len(opening_hours_elements) > 1:
            for section in opening_hours_elements:
                section_title = str(
                    self.encode_remove_eol(section.h3.get_text()))
                if section_title.lower() == 'lounas':
                    opening_times_element = section
        else:
            opening_times_element = opening_hours_elements[0]

        days_hours = self.encode_split_newline(
            opening_times_element.p.get_text())
        days = []
        hours = []
        for elem in days_hours:
            elem_days = elem.split(' ')[0]
            elem_hours = elem.split(' ')[1]
            if '-' in elem_days:
                start_index = days.index(
                    elem_days.split('-')[0].lower())
                end_index = days.index(
                    elem_days.split('-')[1].lower()) + 1
                days.append(weekdays[start_index:end_index])
            else:
                days.append([elem_days.lower()])
            elem_hours = self.sanitize_opening_hour(elem_hours)
            elem_hours = map(parse_hours, elem_hours.split('-'))
            hours.append([elem_hours[0], elem_hours[1]])

    def parse_hours(hours):
        if "." not in str(hours):
            return hours + ".00"
        else:
            return hours

    def sanitize_opening_hour(self, data):
        sanitized = data
        if ' -' in data:
            sanitized = sanitized.replace(' -', '-')
        if '.-' in data:
            sanitized = sanitized.replace('.-', '.00-')
        if data[-1] == '.':
            sanitized[-1] == '.00'

    def parse_restaurant_info(self, soup, url):
        restaurant_elements = soup.select(
            "div#maplist ul.append-bottom li.color")
        try:
            for restaurant in restaurant_elements:
                restaurant_url = self.encode_remove_eol(
                    restaurant.attrs['data-uri'])
                if restaurant_url not in url:
                    pass
                else:
                    name = restaurant.strong.getText()
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
            raise Exception(e)

    def parse_week_number(self, soup):
        head_element = soup.select(
            "#content .pad .head2")[0].getText().encode("utf-8", "ignore")
        week_number = int(re.findall(r"\d\d", head_element)[0])
        self.logger.debug("week number: " + str(week_number))
        return week_number

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

    def encode_split_newline(self, text):
        try:
            return text.encode('utf-8', 'ignore').strip().replace(
                '\t', '').replace('\r', '').split('\n')
        except UnicodeEncodeError, e:
            self.logger.exception(e)
            return text

    def load_page(self, link):
        try:
            self.logger.debug(" Loading page " + link + "...")
            html = requests.get(link)
            self.logger.debug(" Done.")
            return html
        except RequestException, e:
            raise RequestException(e)

    def __repr__(self):
        return "{0} version {1}".format(self.name, __version__)
