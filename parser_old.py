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

# Opening time RegExes
# _OPENING_DATES_REGEX = "(ma|ti|ke|to|pe|la|su)(-(ma|ti|ke|to|pe|la|su))?"
# _OPENING_TIMES_REGEX = "([2][0-4]|[0-1][0-9])(\.[0-5][0-9])?-([2][0-4]|[0-1][0-9])(\.[0-5][0-9])?"
# _OPENINGS_REGEX = _OPENING_DATES_REGEX + "\s" + _OPENING_TIMES_REGEX

# _WEEK_DAYS = ['ma','ti','ke','to','pe','la','su']


class Food(object):
    def __init__(self, name, diets, prices):
        self.name = name
        self.diets = diets
        self.prices = prices


class Restaurant(object):
    def __init__(self, restaurant_name, lunches_by_day):
        self.name = restaurant_name
        self.lunches_by_day = lunches_by_day


class RestaurantDay(object):
    def __init__(self, day_of_the_week, lunches_to_prices, alert):
        self.day_of_the_week = day_of_the_week
        self.lunches_to_prices = lunches_to_prices
        self.alert = alert


class OpeningHours(object):
    def __init__(self, weekDays, hours):
        self.weekDays = weekDays
        self.hours = hours

#
# Parser abstract base class (interface)
#
class Parser(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def __init__(self, week_number, name, version):
        """
        Returns: new parser with proper week number,name and version initialized
        """
        self.week_number = week_number
        self.name = name
        self.version = version

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
    def __init__(self, week_number, name, version):
        super(UnicaParser, self).__init__(int(week_number), str(name), str(version))

    def assure_same_weeknumber(self, soup):
        try:
            string = soup.select("div.pad > h3.head2")[0].get_text().encode("ascii", "ignore")
            current_week_number = int(re.findall(r'\d\d', string)[0])
            if(current_week_number != self.week_number):
                LOG.error(" Expected week number  " + str(
                    self.week_number) + " but was " + str(self.week_number))
                return -1
            else:
                return 0
        except Exception, e:
            LOG.exception(" Exception occured while checking week number\n %s", str(e))
            return -1

    def parse_page(self, page):
        try:
            soup = bs(page, from_encoding='utf-8')
            if self.assure_same_weeknumber(soup) == -1:
                return -1

            
            # contains the lunch menu
            menu_list = soup.select(".menu-list")[0]

            restaurant_name = encode_remove_eol(soup.select(".head")[0].get_text())
            daily_foods = []

            self.opening_hours[restaurant_name] = self.parse_opening_hours(soup)

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
                alert_element = day.table.find("span", { "class" : "alert" })

                lunches_to_prices = []

                day_lunches = [encode_remove_eol(x.get_text() if x else "") for x in lunch_elements]
                day_diets = [encode_remove_eol(x.get_text()) if x.span else "" for x in diet_elements]
                day_prices = [re.findall(r'\d\,\d\d', encode_remove_eol(x.get_text())) for x in price_elements]
                lunches_to_prices = [Food(name, diets, prices) for name, diets, prices in zip(day_lunches, day_diets, day_prices)]

                if (not alert_element) and (len(lunch_elements) is 1) and (len(price_elements) is 1) and (len(day_prices[0]) is 0):
                    LOG.info(" Food without price, handling as alert, restaurant: " + str(restaurant_name) + ", day: " + str(day_element.get_text()))
                    alert = day_lunches[0]
                    daily_foods.append(RestaurantDay(day_number, [], alert))
                elif alert_element:
                    LOG.info(" Inserting alert message, restaurant: " + str(restaurant_name) + ", day: " + str(day_element.get_text()))
                    alert = encode_remove_eol(alert_element.get_text())
                    daily_foods.append(RestaurantDay(day_number, lunches_to_prices, alert))
                else:
                    alert = ""
                    daily_foods.append(RestaurantDay(day_number, lunches_to_prices, alert))

            restaurants_foods = Restaurant(restaurant_name, daily_foods)

            foods_exist = False
            for day in daily_foods:
                if len(day.lunches_to_prices) > 0:
                    foods_exist = True
                    break

            if not foods_exist: 
                return -1
            else:
                return restaurants_foods

        except Exception, e:
            LOG.exception(" Exception occured while parsing... \n %s", str(e))
            return -1

    def parse_opening_hours(self, soup):
        # contains opening hours
        opening_hours_elements = soup.select("#content .pad.mod .threecol")
        section_title = None
        section_contents = []

        # has opening hours and lunch times separately
        if len(opening_hours_elements) > 1:
            
            for section in opening_hours_elements:
                section_title = str(encode_remove_eol(section.h3.get_text()))
                print("section_title: {0}".format(section_title))
                
                if section_title == 'Lounas':
                    
                    if len(section.select("p")) > 1:
                        for text in section.select("p"):
                            section_contents.append(encode_replace_eol(text.get_text().lower()))
                        section_contents = sum(section_contents, [])

                    else:
                        section_contents = encode_replace_eol(section.p.get_text().lower())
        else:
            if(len(opening_hours_elements) == 1):
                section_title = encode_remove_eol(opening_hours_elements[0].h3.get_text())
                section_contents = encode_replace_eol(opening_hours_elements[0].p.get_text().lower())

        print("title: {0}, content: {1}".format(section_title, section_contents))

        return self.format_opening_times(section_contents)

    def format_opening_times(self, unformatted_contents):
        opening_hours = []
        for content in unformatted_contents:
            #remove klo
            content = content.replace(" klo", "")
            if re.match(_OPENINGS_REGEX, content):
                match_object = re.match(_OPENING_DATES_REGEX, content)
                dates = match_object.group()
                dates_split = dates.split("-")
                if len(dates_split) > 1:
                    start_index, end_index = _WEEK_DAYS.index(dates_split[0]), _WEEK_DAYS.index(dates_split[1])
                    #end_index is exclusive
                    dates = ''.join(_WEEK_DAYS[start_index:end_index + 1])
                #openings without dates plus one for space
                times_part = content[match_object.span()[1] + 1:]
                times = re.match(_OPENING_TIMES_REGEX, times_part).group()
                #add trailing zeros if they don't exist
                times_split = times.split("-")
                times_split = [time + ".00" if (len(time) <= 2) else time for time in times_split]
                times = '-'.join(times_split)

                opening_hours.append(OpeningHours(dates, times))
            else:
                break
        #TODO: if empty, log some error

        print(opening_hours)
        return opening_hours

    def parse(self):
        self.opening_hours = {}
        restaurants = []
        for link in rest_urls.UNICA_URLS:
            page = load_page(link)
            output = self.parse_page(page)

            if output == -1:
                LOG.error(" Page that resulted in an error: \n %s", page)
            else:
                restaurants.append(output)

        return restaurants

    def parse_restaurant_datas(self):
        """
        parse() method should be called before this so that opening times are parsed.

        Returns: Parsed restaurant datas
        """
        try:
            page = load_page(rest_urls.UNICA_BASE_URL)
            soup = bs(page, from_encoding='utf-8')
            restaurant_elements = soup.select("div#maplist ul.append-bottom li.color")
            restaurants = []
            for restaurant in restaurant_elements:
                name = encode_remove_eol(restaurant.strong.get_text())
                address = encode_remove_eol(restaurant.attrs['data-address'])
                zip_code = encode_remove_eol(restaurant.attrs['data-zip'])
                post_office = encode_remove_eol(restaurant.attrs['data-city'])
                longitude = encode_remove_eol(restaurant.attrs['data-longitude'])
                latitude = encode_remove_eol(restaurant.attrs['data-latitude'])
                restaurants.append({'name': name, 'address': address, 'zip': zip_code,
                    'postOffice': post_office, 'longitude': longitude, 'latitude': latitude, 'lunchTimes': self.opening_hours[name]})
                # print("Name: {0}, address: {1}, zip: {2}, longitude: {3}, latitude: {4}".format(
                #     name, address, zip_code, longitude, latitude))
            # print(data)
            return restaurants
        except Exception, e:
            LOG.exception(" Exception occured while parsing restaurant\n %s", str(e))
            return -1

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

def encode_replace_eol(text):
    formatted = text.encode('utf-8', 'ignore').strip().replace('\n', '#').replace('\t','').replace('\r', '').replace('\xc2', '').replace('\xa0', '').split('#')
    temp = []
    for text in formatted:
        temp.append(' '.join(text.split()))
    return temp

def combine_restaurants_foods(restaurants):
    """
    Returns: combined foods from list of restaurants to foods by day
    """
    LOG.info(" Combining restaurants...")
    combined_foods = []
    for restaurant in restaurants:
        for day in restaurant.lunches_by_day:
            day_number = day.day_of_the_week
            days_lunches = day.lunches_to_prices
            alert = day.alert

            # inserts a new day if day_number does not exist yet
            if day_number not in range(len(combined_foods)):
                combined_foods.append(
                    {'day': day_number, 'foodsByRestaurant': []})

            combined_foods[day_number]['foodsByRestaurant'].append(
                {'restaurantName': restaurant.name, 'lunches': days_lunches, 'alert': alert})
    return combined_foods

def format_output(restaurants, foods_by_day, parser):
    return {'status': "OK", 'version': parser.version, 'chainName': parser.name, 'foodsByDay': foods_by_day, 'restaurants': restaurants}

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
        parsers = [UnicaParser(week_number, "unica", "0.9")]
    else:
        LOG.error(" Incorrect week number: " + str(week_number) + "\n" + 
            "Week number needs to be in range [1, 52]")
        sys.exit(1)

    for parser in parsers:
        LOG = logging.getLogger(' unica-parser')
        foods = parser.parse()
        restaurants = parser.parse_restaurant_datas()
        foods = combine_restaurants_foods(foods)
        foods = format_output(restaurants, foods, parser)
        json_foods = get_json(foods)
        write_output_file(json_foods, week_number, parser.name)
