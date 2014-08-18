import unittest
import lxml
from bs4 import BeautifulSoup as bs
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
            self.delica = self.read_and_parse_file(
                'tests/resources/delica.html')
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
        """Test that assari's food list is not empty"""
        foodlist_exists = self.unica_parser.assert_foodlist_exist(self.assari)
        assert foodlist_exists

    def test_that_delipharmas_foodlist_is_empty(self):
        """Test that delipharma's food list is empty"""
        foodlist_exists = self.unica_parser.assert_foodlist_exist(
            self.delipharma)
        assert not foodlist_exists

    def test_that_swe_delipharmas_foodlist_is_empty(self):
        """Test that swedish delipharma's food list is empty"""
        foodlist_exists = self.unica_parser.assert_foodlist_exist(
            self.delipharma_swe)
        assert not foodlist_exists

    def test_that_assari_has_6_weekly_foods(self):
        """Test that assari's food list contains 6 foods"""
        foodlist_exists = self.unica_parser.assert_foodlist_exist(
            self.assari)
        weekly_foods = self.unica_parser.parse_foods(
            self.assari)
        assert foodlist_exists
        assert len(weekly_foods) == 6

    def test_that_en_macciavelli_has_5_weekly_foods(self):
        """Test that english macciavelli's food list contains 5 foods"""
        foodlist_exists = self.unica_parser.assert_foodlist_exist(
            self.macciavelli_en)
        weekly_foods = self.unica_parser.parse_foods(
            self.macciavelli_en)
        assert foodlist_exists
        assert len(weekly_foods) == 5

    def test_that_delica_has_alert_on_monday(self):
        """Test that delica has alert element on monday"""
        weekly_foods = self.unica_parser.parse_foods(
            self.delica)
        alert_string = "Deli palvelee viikolla 34 ma-to tervetuloa!"
        test_string = weekly_foods[0].alert
        self.assertEqual(alert_string, test_string)

    def test_that_en_macciavelli_has_no_alerts(self):
        """Test that english macciavelli has no alerts"""
        weekly_foods = self.unica_parser.parse_foods(
            self.macciavelli_en)
        self.assertEqual(weekly_foods[0].alert, "")
        self.assertEqual(weekly_foods[1].alert, "")
        self.assertEqual(weekly_foods[2].alert, "")
        self.assertEqual(weekly_foods[3].alert, "")
        self.assertEqual(weekly_foods[4].alert, "")

    def test_that_assari_is_on_week_33(self):
        """Test that assari's lunch menu is from week 33"""
        week_number = self.unica_parser.parse_week_number(self.assari)
        assert week_number == 33

    def test_that_delica_is_on_week_34(self):
        """Test that delica's lunch menu is from week 34"""
        week_number = self.unica_parser.parse_week_number(self.delica)
        assert week_number == 34
