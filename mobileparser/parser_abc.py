# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class Parser():
    """
    Abstract base class (or interface), which all parsers in the module must
    implement.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, name, version):
        self.name = name
        self.version = version

    @abstractmethod
    def parse_page(self, page):
        """
        Parses given page and returns daily foods as a dictionary of form
        {parser_name: name, parser_version: version, restaurant: Restaurant}

        >>> Unica.parse_page(macciavelli)
        {parser_name: "Unica", parser_version: "0.1.0", restaurant: Restaurant}
        """
        pass

    @abstractmethod
    def parse(self):
        """
        Parses all the restaurants defined in the parser's source, using the
        parse_page(self, page) function.

        >>> Unica.parse()
        {parser_name: "Unica", parser_version: __version__, restaurants: {
        "0": Restaurant(...), "1": ... }}
        """
        pass


class Restaurant(object):
    """
    Represents weekly foods of a given restaurant. weekly_foods consists of
    a dict of Day-objects.
    >>> Restaurant(32, "Delipharma", weekly_foods: {"0": Day(...), "1": ...})
    """
    def __init__(self, restaurant_info, weekly_foods, week_number):
        self.restaurant_info = restaurant_info
        self.weekly_foods = weekly_foods
        self.week_number = week_number


class Day(object):
    """
    Represents a single day of a restaurants food list. daily_foods consists
    of a list of Food-objects.
    >>> Day("Monday", 0, [Food(...), Food(...), ...], "alert?...")
    """
    def __init__(self, name, week_day, daily_foods, alert=""):
        self.name = name
        self.week_day = week_day
        self.daily_foods = daily_foods
        self.alert = alert


class Food(object):
    """
    Represents a single food.
    """
    def __init__(self, name, diets, prices):
        self.name = name
        self.diets = diets
        self.prices = prices
