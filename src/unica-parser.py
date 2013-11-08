from bs4 import BeautifulSoup as BS
import urllib2 as url
import re
import json

page = url.urlopen("http://www.unica.fi/fi/ravintolat/mikro/").read()

soup = BS(page, from_encoding='utf-8')
print soup.original_encoding


menu_list = soup.select(".menu-list")[0]

week_days = menu_list.select(".accord")
restaurant = []
for day in week_days:
	day_name = day.h4.get_text()
	day_number = day.h4.get("data-dayofweek")
	day_lunches = map(lambda x: x.get_text().encode('utf-8', 'ignore'), day.table.select(".lunch")) 
        day_prices = map(lambda y: re.findall(r'\d\,\d\d', y.get_text().encode('ascii','ignore')), day.table.select("[class~=price]"))
	
	
        lunch_price = dict(zip(day_lunches, day_prices))
	restaurant.append({"day": day_name, "foods" : lunch_price})

print json.dumps(restaurant, sort_keys=True, indent=4, separators=(',', ': '))
