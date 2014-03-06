import unittest
import os
from datetime import datetime
from mobilefood_parser.unica_parser import *

def build_relative_path_to(resource):
	return os.path.join(os.path.dirname(__file__), resource)

CURRENT_WEEK_NUMBER = 49
MIKRO_FILE_PATH = build_relative_path_to(os.path.join('resources', 'Mikro_Unica.htm'))
ASSARI_FILE_PATH = build_relative_path_to(os.path.join('resources', 'Assarin_ullakko_Unica.htm'))


class UnicaParserTests(unittest.TestCase):

	def testThatParseShouldFailIfWeekIsNotCurrent(self):
		old_week_number = CURRENT_WEEK_NUMBER - 1
		parser = UnicaParser(week_number=old_week_number)
		test_file = open(MIKRO_FILE_PATH)
		self.assertEquals(-1, parser.parse(test_file))

	def testThatParseFailsWhenDocumentChange(self):
		pass

	def testThatCombineRestaurantsFoodsWorks(self):
		parser = UnicaParser(week_number=CURRENT_WEEK_NUMBER)
		mikro_foods = parser.parse(open(MIKRO_FILE_PATH))
		assari_foods = parser.parse(open(ASSARI_FILE_PATH))
		combined_foods = combine_restaurants_foods([mikro_foods,assari_foods])
		self.assertEquals('Mikro', combined_foods[0]['foods_by_restaurant'][0]['restaurant_name'])

        def ThatParsedRestaurantFoodsContainCorrectInfo(self):
                parser = UnicaParser(week_number=CURRENT_WEEK_NUMBER)
		mikro_foods = parser.parse(open(MIKRO_FILE_PATH))
                self.assertTrue(mikro_foods[0]['lunches_by_day'][0]['lunches_to_prices'][0]['diets'])



if __name__ == '__main__':
    unittest.main()
