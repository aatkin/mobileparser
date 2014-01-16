import unittest
from datetime import datetime
from mobilefood_parser.unica_parser import *


class UnicaParserTests(unittest.TestCase):

	def testThatParseShouldFailIfWeekIsNotCurrent(self):
		current_week_number = 49
		old_week_number = current_week_number - 1
		parser = UnicaParser(week_number=old_week_number)
		test_file = open(build_relative_path_to('resources\\Mikro_Unica.htm'))
		self.assertEquals(-1, parser.parse(test_file))

	def testThatParseFailsWhenDocumentChange(self):
		pass

def build_relative_path_to(resource):
	return os.path.join(os.path.dirname(__file__), resource)

if __name__ == '__main__':
    unittest.main()
