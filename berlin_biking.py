#!/usr/bin/env python
##
## Fetch the police rss feed and look for bike incidents.
## Follow the link and look behind it if it is biking related
##
## Database schema
##
## | ID | DATE | LOCATION | TITLE | LINK | TEXT |


import json
import feedparser
import requests
from lxml import html
import re

import db

"""
Configuration
"""
# police feed
feed_url = "https://www.berlin.de/polizei/polizeimeldungen/index.php/rss"
# search terms
whitelist = ["Fahrrad", "Radfahrer", "Radfahrerin", "Fahrradfahrer", "Fahrradfahrerin", "E-Bike", "Radweg"]
# cookie path
cookie_path = ".berlin_biking.cookie"


def read_cookie():
  try:
    with open(cookie_path, "r") as f:
        return json.load(f)
  except (Exception):
    pass

  return {"last_links": []}


def write_cookie(cookie):
  try:
    with open(cookie_path, "w") as f:
      json.dump(cookie, f)
  except Exception as e:
    print(e)



def check_item(item):
  # look into the content
  content = requests.get(item['link'])
  tree = html.fromstring(content.content)

  # the date
  d = "None"
  for polizeimeldung in tree.xpath('//div[@role = "main"]//div[@class = "polizeimeldung"]/text()'):
    if "Polizeimeldung vom" in polizeimeldung:
      # it is a date
      d = polizeimeldung.split()[-1]
  # the text
  c = tree.xpath('//div[@role = "main"]//div[@class = "textile"]/p/text()')
  text = "".join(c)

  tokens = text.lower().split()
  tokens = [ re.sub(r'\W+', '', tok) for tok in tokens ]

  if any( term.lower() in tokens for term in whitelist):
      return db.Incident(item['title'], "", item['link'], d, text)

  return None


content = feedparser.parse(feed_url)
if not content['feed']:
  print("Failed to fetch rss feed")
else:
  items = content['entries']
  print("Fetched {} items".format(len(items)))

  new_links = []
  incidents = []
  cookie = read_cookie()

  print("New reports:")
  for item in items:
    new_links.append(item['link'])
    if not new_links[-1] in cookie['last_links']:
      i = check_item(item)
      if i:
          print(i)
          incidents.append(i)

  cookie['last_links'] = new_links
  db.s.add_all(incidents)
  db.s.commit()
  write_cookie(cookie)

print("\nDone")
