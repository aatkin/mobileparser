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
