import unittest
import lxml
from bs4 import BeautifulSoup as bs
from mobileparser.unica import Unica
from mobileparser.restaurant_urls import UNICA_RESTAURANTS as unica_urls


class TestUnica(unittest.TestCase):

    def read_and_parse_file(self, file):
        try:
            f = open(file, 'r')
            data = bs(f.read(), "lxml")
            f.close()
            return data
        except Exception, error:
            print error

    def setUp(self):
        self.unica_parser = Unica()
        try:
            self.unica = self.read_and_parse_file(
                'tests/resources/unica.html')
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

    def test_that_assaris_foodlist_isnt_empty(self):
        """Test that assari_fi's food list is not empty"""
        foodlist_exists = self.unica_parser.assert_foodlist_exists(
            self.assari)
        assert foodlist_exists

    def test_that_delipharmas_foodlist_is_empty(self):
        """Test that delipharma_fi's food list is empty"""
        foodlist_exists = self.unica_parser.assert_foodlist_exists(
            self.delipharma)
        assert not foodlist_exists

    def test_that_swe_delipharmas_foodlist_is_empty(self):
        """Test that delipharma_se's food list is empty"""
        foodlist_exists = self.unica_parser.assert_foodlist_exists(
            self.delipharma_swe)
        assert not foodlist_exists

    def test_that_assari_has_6_weekly_foods(self):
        """Test that assari_fi's food list contains 6 foods"""
        weekly_foods = self.unica_parser.parse_foods(
            self.assari)
        assert len(weekly_foods) == 6

    def test_that_en_macciavelli_has_5_weekly_foods(self):
        """Test that macciavelli_en's food list contains 5 foods"""
        weekly_foods = self.unica_parser.parse_foods(
            self.macciavelli_en)
        assert len(weekly_foods) == 5

    def test_that_delica_has_alert_on_monday(self):
        """Test that delica_fi has alert element on monday"""
        weekly_foods = self.unica_parser.parse_foods(
            self.delica)
        alert_string = "Deli palvelee viikolla 34 ma-to tervetuloa!"
        test_string = weekly_foods[0].alert
        self.assertEqual(alert_string, test_string)

    def test_that_en_macciavelli_has_no_alerts(self):
        """Test that macciavelli_en has no alerts"""
        weekly_foods = self.unica_parser.parse_foods(
            self.macciavelli_en)
        self.assertEqual(weekly_foods[0].alert, "")
        self.assertEqual(weekly_foods[1].alert, "")
        self.assertEqual(weekly_foods[2].alert, "")
        self.assertEqual(weekly_foods[3].alert, "")
        self.assertEqual(weekly_foods[4].alert, "")

    def test_that_assari_is_on_week_33(self):
        """Test that assari_fi's lunch menu is from week 33"""
        week_number = self.unica_parser.parse_week_number(self.assari)
        assert week_number == 33

    def test_that_delica_is_on_week_34(self):
        """Test that delica_en's lunch menu is from week 34"""
        week_number = self.unica_parser.parse_week_number(self.delica)
        assert week_number == 34

    def test_that_assaris_info_is_parsed_correctly(self):
        """Test that assari_fi's restaurant info is parsed correctly"""
        data_name = "Assarin ullakko"
        data_latitude = "60.454578973794234"
        data_longitude = "22.287014635968035"
        data_address = "Rehtorinpellonkatu 4 A"
        data_zip = "20500"
        data_city = "Turku"
        assari_url = unica_urls[0]["url_fi"]
        restaurant_info = self.unica_parser.parse_restaurant_info(
            self.unica, assari_url)
        assert data_name == restaurant_info["name"]
        assert data_address == restaurant_info["address"]
        assert data_zip == restaurant_info['zip_code']
        assert data_city == restaurant_info['post_office']
        assert data_longitude == restaurant_info['longitude']
        assert data_latitude == restaurant_info['latitude']
