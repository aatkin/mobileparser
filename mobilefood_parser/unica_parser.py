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
        Returns: restaurant with name and foods and their prices by a day
        """
        restaurants = []

        soup = BS(page, from_encoding='utf-8')

        if self.assureTheWeekNumberIsSameAsInThePage(soup) == -1:
            return -1
        # contains the menu
        menu_list = soup.select(".menu-list")[0]

        foodsByADay = []
        restaurants_foods = {'restaurant_name': soup.select(".head")[
            0].get_text().strip(), 'lunches_by_day': foodsByADay}

        # every day is inside accord
        week_days = menu_list.select(".accord")
        for day in week_days:
            day_number = int(day.h4.get("data-dayofweek"))
            day_lunches = map(lambda x: x.get_text().encode(
                'utf-8', 'ignore'), day.table.select(".lunch"))
            day_prices = map(lambda y: re.findall(
                r'\d\,\d\d', y.get_text().encode('ascii', 'ignore')), day.table.select("[class~=price]"))
            lunches_to_prices = dict(zip(day_lunches, day_prices))
            foodsByADay.append(
                {"day_of_the_week": day_number, "lunches_to_prices": lunches_to_prices})

        return restaurants_foods


def combine_restaurants_foods(restaurants):
    """
    Returns: combined foods from list of restaurants
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

    write_output_file(
        get_json(combine_restaurants_foods(restaurants)), week_number, restaurant_name="unica", file_type="json")
