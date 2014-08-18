import unittest
from bs4 import BeautifulSoup as bs
import lxml
from mobileparser.unica import Unica


class TestUnica(unittest.TestCase):

    def setUp(self):
        self.unica_parser = Unica()
        try:
            self.assari = self.read_and_parse_file(
                'tests/resources/assari.html')
            self.delipharma = self.read_and_parse_file(
                'tests/resources/delipharma.html')
            self.delipharma_swe = self.read_and_parse_file(
                'tests/resources/delipharma_se.html')
            self.macciavelli_en = self.read_and_parse_file(
                'tests/resources/macciavelli_en.html')
        except Exception, error:
            print error

    def read_and_parse_file(self, file):
        try:
            f = open(file, 'r')
            data = bs(f.read(), "lxml")
            f.close()
            return data
        except Exception, error:
            print error

    def test_that_assaris_foodlist_isnt_empty(self):
        foodlist_exists = self.unica_parser.assert_foodlist_exist(self.assari)
        assert foodlist_exists

    def test_that_delipharmas_foodlist_is_empty(self):
        foodlist_exists = self.unica_parser.assert_foodlist_exist(
            self.delipharma)
        assert not foodlist_exists

    def test_that_swe_delipharmas_foodlist_is_empty(self):
        foodlist_exists = self.unica_parser.assert_foodlist_exist(
            self.delipharma_swe)
        assert not foodlist_exists

    def test_that_assari_has_6_weekly_foods(self):
        foodlist_exists = self.unica_parser.assert_foodlist_exist(
            self.assari)
        weekly_foods = self.unica_parser.parse_foods(
            self.assari)
        assert foodlist_exists
        assert len(weekly_foods) == 6

    def test_that_en_macciavelli_has_5_weekly_foods(self):
        foodlist_exists = self.unica_parser.assert_foodlist_exist(
            self.macciavelli_en)
        weekly_foods = self.unica_parser.parse_foods(
            self.macciavelli_en)
        assert foodlist_exists
        assert len(weekly_foods) == 5
