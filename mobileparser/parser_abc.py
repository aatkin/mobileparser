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
    def parse_html(self, html):
        """
        Parses given html and returns daily foods as a dictionary of form
        {parser_name: name, parser_version: version, restaurant: Restaurant}

        >>> Unica.parse_html(macciavelli)
        {parser_name: "Unica", parser_version: "0.1.0", restaurant: Restaurant}
        """
        pass


class Restaurant(object):
    def __init__(self, name, daily_foods):
        self.name = name
        self.daily_foods = daily_foods


class Food(object):
    def __init__(self, name, diets, prices):
        self.name = name
        self.diets = diets
        self.prices = prices
