# mobileparser [![Build Status](https://travis-ci.org/aatkin/mobileparser.png)](https://travis-ci.org/aatkin/mobileparser) #

## Restaurant HTML-parser for Mobilefood project ##

Crawls restaurant web pages for relevant food lists and extracts them into usable JSON-formatted data.

  * Create virtualenv folder if you haven't already: `virtualenv env` and then activate it: `source env/Scripts/activate`
  * Install requirements using pip: `pip install -r requirements.txt`
  * Run app: `python mobileparser/main.py`
  * [OPTIONAL] Use grunt-watch for automatically running tests each time tests are modified: `npm install && grunt`