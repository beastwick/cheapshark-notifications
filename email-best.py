#import pdb

import json
import pprint
import requests
import subprocess
from operator import itemgetter

def storeText(id):
  match int(id):
    case 1:
      return "Steam"
    case 2:
      return "GamersGate"
    case 3:
      return "GreenManGaming"
    case 7:
      return "GOG"
    case 8:
      return "Origin"
    case 11:
      return "Humble Bundle"
    case 13:
      return "Ubisoft Store"
    case 15:
      return "Fanatical"
    case 21:
      return "WinGameStore"
    case 23:
      return "GameBillet"
    case 24:
      return "Voidu"
    case 25:
      return "Epic Games"
    case 27:
      return "Gamesplanet"
    case 28:
      return "Gamesload"
    case 30:
      return "IndieGala"
    case 31:
      return "Blizzard Shop"
    case 33:
      return "DLGamer"
    case 34:
      return "Noctre"
    case 35:
      return "DreamGame"
    case _:
      return "Check Cheapshark.com for originating site."

resp = requests.get(url='https://www.cheapshark.com/api/1.0/deals?&pageSize=60&pageNumber=0')
data = resp.json()

games = []

for deal in data:
  if float(deal['dealRating']) >= 9.0 or (float(deal['dealRating']) >= 8.0 and int(deal['metacriticScore']) >= 90):
    details = (deal['gameID'], deal['title'], float(deal['salePrice']), storeText(deal['storeID']), deal['metacriticScore'])
    games.append(details)

games = set(games)
games = sorted(games, key=itemgetter(2,4))

for game in games:
    print('$' + format(game[2], '.2f') + ', ' + game[1] + ', ' + game[3])

#subprocess.Popen['/bin/sh', '-c', 'sh email-best']
