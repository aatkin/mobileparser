import unittest
from bs4 import BeautifulSoup as bs
from mobileparser.unica import Unica


class TestUnica(unittest.TestCase):

    def setUp(self):
        self.unica_parser = Unica()
        try:
            f = open('tests/resources/assari.html', 'r')
            self.assari = bs(f.read())
            f.close()
            f = open('tests/resources/delipharma.html', 'r')
            self.delipharma = bs(f.read())
            f.close()
        except Exception, error:
            print error

    def test_assaris_foodlist_isnt_empty(self):
        foodlist_exists = self.unica_parser.assert_foodlist_exist(self.assari)
        assert foodlist_exists

    def test_delipharmas_foodlist_is_empty(self):
        foodlist_exists = self.unica_parser.assert_foodlist_exist(
            self.delipharma)
        assert not foodlist_exists
