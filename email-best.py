import requests
import json
import pprint
from operator import itemgetter

resp = requests.get(url='https://www.cheapshark.com/api/1.0/deals?&pageSize=60&pageNumber=0')
data = resp.json()
games = []

for deal in data:
  if float(deal['dealRating']) > 8.0 and int(deal['metacriticScore']) > 60:
    details = (deal['gameID'], deal['title'], float(deal['salePrice'])) #, deal['storeID'])
    games.append(details)

games = set(games)
games = sorted(games, key=itemgetter(2,0))

prev=''
for game in games:
  if (prev != game[1]):
    prev = game[1]
    print(game[1] + ', $' + format(game[2], '.2f'))
  else:
    continue
    

#def storeText(id):
  #id = id - 1
  #match id:
    #case 0:
      #return "steam"
    #case 1:
      #return "gamersgate"
    #case 2:
      #return "greenmangaming"
    #case 3:
      #return ""
    #case 4:
    #case 5:
    #case 6:
    #case 7:
    #case 8:
    #case 9:
    #case 10:
    #case 11:
    #case 12:
    #case 13:
    #case 14:
    #case 15:
    #case 16:
    #case 17:
    #case 18:
    #case 19:
    #case 20:
    #case 21:
    #case 22:
    #case 23:
    #case 24:
    #case 25:
    #case 26:
    #case 27:
    #case 28:
    #case 29:
    #case _:
