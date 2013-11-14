from bs4 import BeautifulSoup as BS
import urllib2 as url
import re, json, os
import restaurant_urls as rest_urls

restaurants = []

for link in rest_urls.UNICA_URLS:
	print "loading page..."
	page = url.urlopen(link).read()

	soup = BS(page, from_encoding='utf-8')

	#contains the menu
	menu_list = soup.select(".menu-list")[0]

	restaurant_foods = []
	restaurant = {"name" : soup.select(".head")[0].get_text().strip(), "days" : restaurant_foods}

	#every day is inside accord
	week_days = menu_list.select(".accord")
	for day in week_days:
	    day_name = day.h4.get_text()
	    day_number = day.h4.get("data-dayofweek")
	    day_lunches = map(lambda x: x.get_text().encode('utf-8', 'ignore'), day.table.select(".lunch")) 
	    day_prices = map(lambda y: re.findall(r'\d\,\d\d', y.get_text().encode('ascii','ignore')), day.table.select("[class~=price]"))
	    lunch_price = dict(zip(day_lunches, day_prices))
	    restaurant_foods.append({"day": day_name, "foods" : lunch_price})

	restaurants.append(restaurant)

	print "creating json format..."
	json_format = json.dumps(restaurant, sort_keys=True, indent=4, separators=(',', ': '))

	directory = '../output/' + restaurant['name']
	if not os.path.exists(directory):
	    os.makedirs(directory)

	print "writing to file..."
	open(directory + restaurant['name'] + ".json","w+").write(json_format)

for rest in restaurants:
	print rest['days'][0]['day']
	print rest['days'][0]['foods']
