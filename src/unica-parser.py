from bs4 import BeautifulSoup as BS
import urllib2 as url

page = url.urlopen("http://www.unica.fi/fi/ravintolat/mikro/", data="UTF-8").read()
print page

