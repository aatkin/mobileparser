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
        LOG.exception("Connection failed to UNICA")
        return

    return BS(page, from_encoding='utf-8')


def parse(expected_week_number):
    """
    """
    restaurants = []

    for link in rest_urls.UNICA_URLS:
        soup = load_page(link)

        week_number = int(
            re.findall(r'\d\d', soup.select("div.pad > h3.head2")[0].get_text().encode('ascii', 'ignore'))[0])
        if(week_number != expected_week_number):
            LOG.error(' Expected week number was ' + str(
                expected_week_number) + ' but actual was ' + str(week_number))
            return
        # contains the menu
        menu_list = soup.select(".menu-list")[0]

        restaurant_foods = []
        restaurant = {"name": soup.select(".head")[
                      0].get_text().strip(), "days": restaurant_foods}

        # every day is inside accord
        week_days = menu_list.select(".accord")
        for day in week_days:
            day_number = int(day.h4.get("data-dayofweek"))
            day_lunches = map(lambda x: x.get_text().encode(
                'utf-8', 'ignore'), day.table.select(".lunch"))
            day_prices = map(lambda y: re.findall(
                r'\d\,\d\d', y.get_text().encode('ascii', 'ignore')), day.table.select("[class~=price]"))
            lunch_price = dict(zip(day_lunches, day_prices))
            restaurant_foods.append(
                {"day": day_number, "foods": lunch_price})

        restaurants.append(restaurant)

        write_output_file(
            get_json(restaurant), week_number, restaurant_name=restaurant['name'], file_type="json")

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
    parse(int(sys.argv[1]))
