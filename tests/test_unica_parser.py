import unittest
import os
from datetime import datetime
from mobilefood_parser import parser as p
import re

def build_relative_path_to(resource):
	return os.path.join(os.path.dirname(__file__), resource)

CURRENT_WEEK_NUMBER = 49
MIKRO_FILE_PATH = build_relative_path_to(os.path.join('resources', 'Mikro_Unica.htm'))
ASSARI_FILE_PATH = build_relative_path_to(os.path.join('resources', 'Assarin_ullakko_Unica.htm'))


class UnicaParserTests(unittest.TestCase):

	def testThatOpeningDatesAreDiscoveredCorrectly(self):
		test_openings = "ma-to 10.30-14.30"
		self.assertEquals(re.match(p._OPENING_DATES_REGEX, test_openings).group(), "ma-to")

	def testThatOpeningTimesAreDiscoveredCorrectly(self):
		test_opening_times = "10.30-14.30"
		self.assertEquals(re.match(p._OPENING_TIMES_REGEX, test_opening_times).group(), "10.30-14.30")

	def testThatOpeningTimesStringIsMatchedWithLongFormat(self):
		test_openings = "ma-to 10.30-14.30"
		self.assertEquals(re.match(p._OPENINGS_REGEX, test_openings).group(), "ma-to 10.30-14.30")

	def testThatOpeningTimesStringIsMatchedWithShortFormat(self):
		test_openings = "la 11-16"
		self.assertEquals(re.match(p._OPENINGS_REGEX, test_openings).group(), "la 11-16")

	def testThatOpeningTimesStringIsMatchedWithNonCompleteFormat(self):
		test_openings = "pe 10.30-16"
		self.assertEquals(re.match(p._OPENINGS_REGEX, test_openings).group(), "pe 10.30-16")

	def testThatOpeningTimesStringIsMatchedAndExtraDotIsIgnored(self):
		test_openings = "pe 10.30-16."
		self.assertEquals(re.match(p._OPENINGS_REGEX, test_openings).group(), "pe 10.30-16")

	def testThatParseShouldFailIfWeekIsNotCurrent(self):
		old_week_number = CURRENT_WEEK_NUMBER - 1
		parser = p.UnicaParser(week_number=old_week_number)
		test_file = open(MIKRO_FILE_PATH)
		self.assertEquals(-1, parser.parse(test_file))

	def testThatParseFailsWhenDocumentChange(self):
		pass

	def testThatCombineRestaurantsFoodsWorks(self):
		parser = p.UnicaParser(week_number=CURRENT_WEEK_NUMBER)
		mikro_foods = parser.parse(open(MIKRO_FILE_PATH))
		assari_foods = parser.parse(open(ASSARI_FILE_PATH))
		combined_foods = p.combine_restaurants_foods([mikro_foods,assari_foods])
		self.assertEquals('Mikro', combined_foods[0]['foods_by_restaurant'][0]['restaurant_name'])

        def ThatParsedRestaurantFoodsContainCorrectInfo(self):
                parser = p.UnicaParser(week_number=CURRENT_WEEK_NUMBER)
		mikro_foods = parser.parse(open(MIKRO_FILE_PATH))
                self.assertTrue(mikro_foods[0]['lunches_by_day'][0]['lunches_to_prices'][0]['diets'])



if __name__ == '__main__':
    unittest.main()
