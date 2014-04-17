#!/usr/bin/python

from bs4 import BeautifulSoup as bs
import urllib2 as url
import re
import json, jsonpickle
import os
import sys
from abc import ABCMeta, abstractmethod
from datetime import datetime
import logging
import restaurant_urls as rest_urls

logging.basicConfig(level=logging.INFO)

_OUTPUTDIR = "../output"

#
# Food-class
# 
class Food(object):
    def __init__(self, name, diets, prices):
        self.name = name
        self.diets = diets
        self.prices = prices

class Restaurant(object):
    def __init__(self, restaurant_name, lunches_by_day):
        self.name = restaurant_name
        self.lunches_by_day = lunches_by_day

# 
# Parser abstract base class (interface)
# 
class Parser(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, week_number, name):
        """
        Returns: new parser with proper week number and name initialized
        """
        self.week_number = week_number
        self.name = name

    @abstractmethod
    def parse(self):
        """
        Returns: all restaurants datas as [{restaurant_name: name, lunches_by_day: foods}, ...]
        """
        pass

    @abstractmethod
    def parse_page(self, page):
        """
        Returns: single restaurants data as {restaurant_name: name, lunches_by_day: foods}
        """
        pass

# 
# Unica-parser, implements Parser abstract base class
# 
class UnicaParser(Parser):
    def __init__(self, week_number, name):
        super(UnicaParser, self).__init__(int(week_number), str(name))

    def assure_same_weeknumber(self, soup):
        string = soup.select("div.pad > h3.head2")[0].get_text().encode("ascii", "ignore")
        current_week_number = int(re.findall(r'\d\d', string)[0])
        if(current_week_number != self.week_number):
            LOG.error(" Expected week number  " + str(
                self.week_number) + " but was " + str(self.week_number))
            return -1
        else:
            return 0

    def parse_page(self, page):
        try:
            soup = bs(page, from_encoding='utf-8')
            if self.assure_same_weeknumber(soup) == -1:
                return -1
            
            # contains the lunch menu
            menu_list = soup.select(".menu-list")[0]

            restaurant_name = encode_remove_eol(soup.select(".head")[0].get_text())
            daily_foods = []

            # every day is inside accord-div
            week_days = menu_list.select(".accord")

            if len(week_days) == 0:
                LOG.error(" Weekdays inside accord not found. Maybe page HTML has changed?")
                return -1

            for day in week_days:
                day_element = day.h4
                LOG.info(" Parsing weekday: %s", day.h4.get_text())
                
                day_number = int(day_element.get("data-dayofweek"))

                lunch_elements = day.table.select(".lunch")
                diet_elements = day.table.select(".limitations")
                price_elements = day.table.select(".price")
                alert_elements = day.table.select(".alert")

                lunches_to_prices = []

                day_lunches = [encode_remove_eol(x.get_text() if x else "") for x in lunch_elements]
                day_diets = [encode_remove_eol(x.get_text()) if x.span else "" for x in diet_elements]
                day_prices = [re.findall(r'\d\,\d\d', encode_remove_eol(x.get_text())) for x in price_elements]
                lunches_to_prices = [Food(name, diets, prices) for name, diets, prices in zip(day_lunches, day_diets, day_prices)]

                if (len(alert_elements) > 0) or (len(lunch_elements) < 1):
                    LOG.info(" Inserting alert = true, restaurant: " + str(restaurant_name) + ", day: " + str(day_element))
                    daily_foods.append({"day_of_the_week": day_number, "lunches_to_prices": lunches_to_prices, "alert": True})
                else:
                    daily_foods.append({"day_of_the_week": day_number, "lunches_to_prices": lunches_to_prices, "alert": False})

            restaurants_foods = Restaurant(restaurant_name, daily_foods)

            foods_exist = False
            for day in daily_foods:
                if len(day["lunches_to_prices"]) > 0:
                    foods_exist = True
                    break

            if not foods_exist: 
                return -1
            else:
                return restaurants_foods

        except Exception, e:
            LOG.exception(" Exception occured while parsing... \n %s", str(e))
            return -1

    def parse(self):
        restaurants = []
        for link in rest_urls.UNICA_URLS:
            page = load_page(link)
            output = self.parse_page(page)

            if output == -1:
                LOG.error(" Page that resulted in an error: \n %s", page)
            else:
                restaurants.append(output)

        return restaurants

# 
# Static methods
# 

def load_page(link):
    page = None
    try:
        LOG.info(" Loading page... " + link)
        page = url.urlopen(link).read()
    except url.URLError, e:
        LOG.exception(" Unable to connect to a given link: \n %s", str(e))
        return -1
    return page

def encode_remove_eol(text):
    """
    Encodes text to UTF-8 and removes End-of-Line 
    characters in the middle and leading and trailing spaces. 
    """
    return text.encode('utf-8', 'ignore').strip().replace('\n', '').replace('\t','').replace('\r', '')

def combine_restaurants_foods(restaurants):
    """
    Returns: combined foods from list of restaurants to foods by day
    """
    LOG.info(" Combining restaurants...")
    combined_foods = []
    for restaurant in restaurants:
        restaurant_name = restaurant.name
        for day in restaurant.lunches_by_day:
            day_number = day['day_of_the_week']
            days_lunches = day['lunches_to_prices']
            alert = day['alert']

            if day_number not in range(len(combined_foods)):
                combined_foods.append(
                    {'day': day_number, 'foods_by_restaurant': []})

            combined_foods[day_number]['foods_by_restaurant'].append(
                {'restaurant_name': restaurant_name, 'foods': days_lunches, 'alert': alert})
    return combined_foods

def get_json(data):
    LOG.info(" Creating json format...")
    return jsonpickle.encode(data, unpicklable=False);

def write_output_file(data, week_number, restaurant_name="default", file_type="json"):
    year_and_week = str(datetime.now().year) + "_w" + str(week_number)
    restaurant_name = format_string(restaurant_name)
    directory = _OUTPUTDIR + '/%s' % restaurant_name

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = "%(dir)s/%(filename)s.%(filetype)s" % {
        'dir': directory, 'filename': year_and_week + "_" + restaurant_name, 'filetype': file_type}

    try:
        LOG.info(" Writing to a file: " + filename)
        open(filename, "w+").write(data)
    except Exception, e:
        LOG.exception(" Exception occurred while writing to file: \n %s", str(e))
        return -1

def format_string(string):
    return string.strip().replace(" ", "_")

# 
# Main-method
# 
if __name__ == '__main__':
    LOG = logging.getLogger(' main-parser')
    if len (sys.argv) > 1:
        try:
            week_number = int(sys.argv[1])
        except ValueError:
            LOG.error(" Incorrect week number: " + str(sys.argv[1]))
            sys.exit(1)
    else:
        week_number = datetime.now().isocalendar()[1]

    if week_number >= 1 and week_number <= 52:
        parsers = [UnicaParser(week_number, "unica")]
    else:
        LOG.error(" Incorrect week number: " + str(week_number) + "\n" + 
            "Week number needs to be in range [1, 52]")
        sys.exit(1)

    for parser in parsers:
        LOG = logging.getLogger(' unica-parser')
        foods = parser.parse()
        foods = combine_restaurants_foods(foods)
        json_foods = get_json(foods)
        write_output_file(json_foods, week_number, parser.name)
