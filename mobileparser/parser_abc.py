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


class Week(object):
    """
    Represents weekly foods of a given restaurant. weekly_foods consists of
    a list of Day-objects.
    >>> Week(32, "Unica", [Day(...), Day(...), ...])
    """
    def __init__(self, week_number, restaurant_name, weekly_foods):
        self.week_number = week_number
        self.restaurant_name = restaurant_name
        self.daily_foods = daily_foods


class Day(object):
    """
    Represents a single day of a restaurants food list. daily_foods consists
    of a list of Food-objects.
    >>> Day("Monday", 0, [Food(...), Food(...), ...])
    """
    def __init__(self, name, week_day, daily_foods):
        self.name = name
        self.week_day = week_day
        self.daily_foods = daily


class Food(object):
    """
    Represents a single food.
    """
    def __init__(self, name, diets, prices):
        self.name = name
        self.diets = diets
        self.prices = prices
