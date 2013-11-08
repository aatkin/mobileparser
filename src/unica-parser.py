from bs4 import BeautifulSoup as BS
import urllib2 as url

page = url.urlopen("http://www.unica.fi/fi/ravintolat/mikro/", data="UTF-8").read()

soup = BS(page)

menu_list = soup.select(".menu-list")[0]
week_days = menu_list.select(".accord")
for day in week_days:
	print day.h4.get_text()
	print day.table.get_text()
print soup.select("#side-navi")[0].find_all("li")[0].get_text()

