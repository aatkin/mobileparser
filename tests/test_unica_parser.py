import unittest
from datetime import datetime
from mobilefood_parser import unica_parser

class UnicaParserTests(unittest.TestCase):

	def testThatParseShouldFailIfWeekIsNotCurrent(self):
		year, week_number, week_day = datetime.now().isocalendar()
		old_week_number = week_number - 1 
		self.assertEquals(unica_parser.parse(old_week_number), -1)

if __name__ == '__main__':
    unittest.main()

