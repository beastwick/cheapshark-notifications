#import pdb

import json
import os
import re
import requests
import subprocess

from operator import itemgetter

def email(to, subject, body):
    os.system('echo "{body}" | mail -s "{subject}" "{to}"'.format(to=to, subject=subject, body=body))

with open("config.json", "r") as jsonfile:
    email_config = json.load(jsonfile)

def storeText(id):
  if id ==  1:
    return "Steam"
  elif id == 2:
    return "GamersGate"
  elif id == 3:
    return "GreenManGaming"
  elif id == 7:
    return "GOG"
  elif id == 8:
    return "Origin"
  elif id == 11:
    return "Humble Bundle"
  elif id == 13:
    return "Ubisoft Store"
  elif id == 15:
    return "Fanatical"
  elif id == 21:
    return "WinGameStore"
  elif id == 23:
    return "GameBillet"
  elif id == 24:
    return "Voidu"
  elif id == 25:
    return "Epic Games"
  elif id == 27:
    return "Gamesplanet"
  elif id == 28:
    return "Gamesload"
  elif id == 29:
    return "2Game"
  elif id == 30:
    return "IndieGala"
  elif id == 31:
    return "Blizzard Shop"
  elif id == 33:
    return "DLGamer"
  elif id == 34:
    return "Noctre"
  elif id == 35:
    return "DreamGame"
  else: 
    return "Check Cheapshark.com for originating site."

resp = requests.get(url='https://www.cheapshark.com/api/1.0/deals?&pageSize=60&pageNumber=0')
data = resp.json()

games = []
for deal in data:
  if float(deal['dealRating']) >= 9.0 or (float(deal['dealRating']) >= 8.0 and int(deal['metacriticScore']) >= 90):
    details = (deal['gameID'], deal['title'], float(deal['salePrice']), storeText(int(deal['storeID'])), deal['metacriticScore'])
    games.append(details)

games = set(games)
games = sorted(games, key=itemgetter(2,4))

sales = []
for game in games:
  metacritic = ''
  if int(game[4]) > 0:
    metacritic = ', ' + game[4]

  sales.append('$' + format(game[2], '.2f') + ', ' + game[1] + ', ' + game[3] + metacritic + '\n') 

prev = (open('prev', 'r')).readlines()

# From here onwards, we are only interested in free $0.00 games.
# Taken from free and not sales, because the script was altered to just care about free items.

# What is free.
free = []
for entry in sales:
  if re.match(r'.*\$0\.00.*', entry):
    free.append(re.sub(r'.*\$0\.00, ', '', entry)) 

# What is new.
new = free.copy()
for old in prev:
  if old in new:
    new.remove(old) # Only considered new if it has not been seen before.

# What is gone.
gone = prev.copy()
if prev:
  for sale in free:
    if sale in gone:
      gone.remove(sale) # What is left in this list is gone, it did not appear in the new list.

# What is the same.
same = []
for sale in free:
  if sale in prev:
    if re.match(r'.*\$0\.00.*', sale):
      continue
    same.append(sale)

# Save the current list of games that met all our criteria.
prev =(open('prev', 'w'))
for sale in free:
  prev.write(sale)
prev.close()

body = ''

#if free:
  #body += "Free:\n"
  #for entry in free:
    #body += entry
  #body += "\n"

if new:
  body += "New:\n"
  for entry in new:
    body += entry
  body += "\n"

if gone:
  body += "Gone:\n"
  for entry in gone:
    body += entry
  body += "\n"

#if same:
  #body += "Same:\n"
  #for entry in same:
    #body += entry
  #body += "\n"

if len(body):
    email(email_config['to'], email_config['subject'], body)
else:
    print('nothing to send')
