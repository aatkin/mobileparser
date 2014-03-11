#!/usr/bin/python 

from bs4 import BeautifulSoup as BS
import urllib2 as url
import re
import json
import os
import sys
from datetime import datetime
import logging
import restaurant_urls as rest_urls

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(' unica-parser ')


def load_page(link):
    page = None

    try:
        LOG.info(" Loading page... " + link)
        page = url.urlopen(link).read()

    except url.URLError, e:
        LOG.exception("Unable to connect to a given link: \n %s", str(e))
        return -1

    return page


class UnicaParser:

    def __init__(self, week_number):
        self.week_number = week_number

    def assureTheWeekNumberIsSameAsInThePage(self, soup):
        current_week_number = int(
            re.findall(r'\d\d', soup.select("div.pad > h3.head2")[0].get_text().encode('ascii', 'ignore'))[0])
        if(current_week_number != self.week_number):
            LOG.error(' Expected week number was ' + str(
                self.week_number) + ' but actual was ' + str(self.week_number))
            return -1
        else:
            return 0

    def parse(self, page):
        """
        Returns: restaurant with name and foods and their prices by a day
        """

        try:
            soup = BS(page, from_encoding='utf-8')
        
            if self.assureTheWeekNumberIsSameAsInThePage(soup) == -1:
                return -1
            
            # contains the lunch menu
            menu_list = soup.select(".menu-list")[0]

            restaurant_name = removeEOLAndEncode(soup.select(".head")[0].get_text())
            foodsByADay = []
            restaurants_foods = {'restaurant_name': restaurant_name, 'lunches_by_day': foodsByADay}

            # every day is inside accord
            week_days = menu_list.select(".accord")

            if len(week_days) == 0:
                LOG.error("Week days in accordion can't be found. Check page whether its HTML has changed!")
                return -1

            for day in week_days:
                day_element = day.h4
                LOG.info(" Parsing week day: %s", day.h4.get_text())
                
                day_number = int(day_element.get("data-dayofweek"))

                lunch_elements = day.table.select(".lunch")
                diet_elements = day.table.select(".limitations")
                price_elements = day.table.select(".price")

                if len(lunch_elements) == 0 or not len(lunch_elements) == len(diet_elements) == len(price_elements):
                    error_message = " Problem detected while parsing foods:"
                    if len(lunch_elements) == 0:
                        error_message = error_message + " Food names could not be parsed."

                    if len(diet_elements) == 0:
                        error_message = error_message + " Diets could not be parsed."
               
                    if len(price_elements) == 0:
                        error_message = error_message + " Prices could not be parsed."
                    
                    LOG.error(error_message)
                    LOG.error("Day that could not be parsed:\n %s", day)
                    return -1


                day_lunches = [removeEOLAndEncode(x.get_text() if x else "") for x in lunch_elements]

                day_diets = [removeEOLAndEncode(x.get_text()) if x.span else "" for x in diet_elements]

                day_prices = [re.findall(r'\d\,\d\d', removeEOLAndEncode(x.get_text())) for x in price_elements]

            
                lunches_to_prices = [{'name' : food, 'diets' : diets,'prices' : prices} for food, diets, prices in zip(day_lunches, day_diets, day_prices)]
            
                foodsByADay.append({"day_of_the_week": day_number, "lunches_to_prices": lunches_to_prices})

            return restaurants_foods

        except Exception, e:
            LOG.exception("Exception occured while parsing... \n %s", str(e))
            return -1
        

def removeEOLAndEncode(text):
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
    for rest in restaurants:
        rest_name = rest['restaurant_name']
        for day in rest['lunches_by_day']:
            day_number = day['day_of_the_week']
            days_lunches = day['lunches_to_prices']

            if day_number not in range(len(combined_foods)):
                combined_foods.append(
                    {'day': day_number, 'foods_by_restaurant': []})

            combined_foods[day_number]['foods_by_restaurant'].append(
                {'restaurant_name': rest_name, 'foods': days_lunches})
    return combined_foods


def get_json(data):
    """
        Creates and returns a json from data.
        Parameters
        -----------
    data: Object
    Returns
    --------
    data: Object
    data in json format
        """
    LOG.info(" Creating json format...")
    return json.dumps(data)


def write_output_file(data, week_number, restaurant_name="", file_type="json"):
    """
    Writes data to file that is placed in output directory.
    Parameters
    -----------
    data: Object
    restaurant_name: str
    file_type: str
    """
    year_and_week = str(datetime.now().year) + "_w" + str(week_number)
    restaurant_name = format_name(restaurant_name)
    directory = '../output/%s' % restaurant_name
    # make the directory above if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = "%(dir)s/%(filename)s.%(filetype)s" % {
        'dir': directory, 'filename': year_and_week + "_" + restaurant_name, 'filetype': file_type}

    LOG.info(" Writing to a file: " + filename)
    # Write with w+ rights
    open(filename, "w+").write(data)


def format_name(name):
    """
    Formats string to filename compatible format.
    Parameters
    -----------
    name: str
    Returns
    --------
    name: str
    Formatted name
    """
    return name.strip().replace(" ", "_")

if __name__ == '__main__':
    if len (sys.argv) > 1:
        week_number = int(sys.argv[1])
    else:
        week_number = datetime.now().isocalendar()[1]

    if week_number >= 1 and week_number <= 52:
        LOG.info(" Parsing Unica-foods from week " + str(week_number))
        parser = UnicaParser(week_number)
    else:
        sys.exit(1)

    restaurants = []

    for link in rest_urls.UNICA_URLS:
        page = load_page(link)
        output = parser.parse(page)

        if output == -1:
            sys.exit(1)
        else:
            restaurants.append(output)

    try:
        write_output_file(
            get_json(combine_restaurants_foods(restaurants)), week_number, restaurant_name="unica", file_type="json")
    except Exception, e:
        LOG.exception("Exception occured while combining foods and writing them to file: \n %s", str(e))
