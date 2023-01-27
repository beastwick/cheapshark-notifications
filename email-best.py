#import pdb

import json
import re
import requests
import subprocess

from operator import itemgetter

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

# What is free.
free = []
for entry in sales:
  if re.match(r'.*\$0\.00.*', entry):
    free.append(entry) 

# What is new.
new = sales.copy()
for old in prev:
  if old in new:
    new.remove(old)

# What is gone.
gone = prev.copy()
if prev:
    for sale in sales:
      if sale in gone:
        gone.remove(sale)

# What is the same.
same = []
for sale in sales:
  if sale in prev:
    if re.match(r'.*\$0\.00.*', sale):
      continue
    same.append(sale)

prev =(open('prev', 'w'))
for sale in sales:
  prev.write(sale)
prev.close()

if free:
  print('\nFree:\n')
  for entry in free:
    print(entry, end='')

if new:
  print('\nNew:\n')
  for entry in new:
    print(entry, end='')

if gone:
  print('\nGone:\n')
  for entry in gone:
    print(entry, end='')
    
if same:
  print('\nSame:\n')
  for entry in same:
    print(entry, end='')
