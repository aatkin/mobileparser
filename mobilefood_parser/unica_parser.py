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
        LOG.exception("Unable to connect to a given link")
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
        Returns: list of foods by a day
        """
        restaurants = []

        soup = BS(page, from_encoding='utf-8')

        if self.assureTheWeekNumberIsSameAsInThePage(soup) == -1:
            return -1
        # contains the menu
        menu_list = soup.select(".menu-list")[0]
        
        foodsByADay = []
        restaurants_foods = {'restaurant_name' : soup.select(".head")[
            0].get_text().strip(), 'lunches_by_day' : foodsByADay}

        # every day is inside accord
        week_days = menu_list.select(".accord")
        for day in week_days:
            day_number = int(day.h4.get("data-dayofweek"))
            day_lunches = map(lambda x: x.get_text().encode(
                'utf-8', 'ignore'), day.table.select(".lunch"))
            day_prices = map(lambda y: re.findall(
                r'\d\,\d\d', y.get_text().encode('ascii', 'ignore')), day.table.select("[class~=price]"))
            lunches_to_prices = dict(zip(day_lunches, day_prices))
            foodsByADay.append({"day_of_the_week" : day_number, "food": lunches_to_prices})

        write_output_file(
            get_json(restaurants_foods), self.week_number, restaurant_name=restaurants_foods['restaurant_name'], file_type="json")

        """
        # daily foods in one file for now
        week_day_all = []
        for rest in restaurants:
            rest_name = rest['name']
            for day in rest['days']:
                day_number = day['day']
                day_foods = day['foods']

                if day_number not in range(len(week_day_all)):
                    week_day_all.append({'day': day_number, 'restaurants': []})

                week_day_all[day_number]['restaurants'].append(
                    {'restaurant': rest_name, 'foods': day_foods})

        write_output_file(
            get_json(week_day_all), week_number, restaurant_name="unica", file_type="json")
        """


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
    # Write with w+ writes
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
    # parse(datetime.datetime.now().isocalendar()[1])
    parser = UnicaParser(int(sys.argv[1]))
    for link in rest_urls.UNICA_URLS:
        #sys.exit(parser.parse(load_page(link)))
        parser.parse(load_page(link))
