from pymongo import MongoClient
from bson.json_util import dumps
import pymongo
client = MongoClient('mongodb+srv://klaas:root@clusterteamproject.y22lv.mongodb.net/test')
mydb = client["TeamProjectTiktem"]
games = mydb["Games"]
scores = mydb["Scores"]
# print(client.list_database_names())
def instergames():
    data ={"game":"Speedrun","info":{"description":"Deze game bestaat uit een vast parcour van een aantal oplichtende Tik’s. Hoe sneller je dit parcour  doet hoe hoger je score.","gameid":1}},{"game":"Simon says","info":{"description":"Je begint met 1 Tik die een kleur toont die je moet aantikken, per keer dat je het juist hebt komt er een extra Tik bij. Dit blijft zicht herhalen tot je een fout maakt. Scoreboard houdt bij hoeveel Tik's je hebt kunnen onthouden.","gameid":2}},{"game":"Tik tak boem","info":{"description":"Tik's veranderen van groen naar rood, en flikkeren/piepen. Hoe sneller ze flikkeren/piepen hoe sneller ze van groen naar rood veranderen.  Bij het tikken van de Tik wordt deze terug gereset. De score hangt af van hoelang je het kan volhouden voor er eentje 'ontploft'.","gameid":3}},{"game":"Color hunt","info":{"description":"Iedere Tik zal een verschillende kleur krijgen als je deze aantikt krijg je een score die bij die kleur past. De kleuren zullen na een bepaalde tijd veranderen dus wees snel. De bedoeling is om zoveel mogelijk punten te krijgen in een bepaalde tijd","gameid":4}},{"game":"Color team","info":{"description":"spel voor 1 tot 3 spelers. Elke speler heeft een kleur, bij de start van de ronde licht er van elk kleur 1 Tik op. Bij het tikken van deze Tik licht er een nieuwe op, op een andere locatie. De speler met het meeste  aantal aangeraakte Tik’s wint.","gameid":5}},{"game":"Simon says versus","info":{"description":"spel voor 2 + spelers. Speler 1 begint & mag 1 Tik aantikken, dan moet speler 2 deze Tik aanraken & de 2de kiezen. Speler 3 moet de eerste 2 aantikken en kiest de derde enz. De speler die een fout maakt valt af.","gameid":6}}
    x = games.insert_many(data)
# for x in games.find():
#     print(x)

# score = {"name": "Klaas", "score": 4.948, "gameid": 1, "scoretype" : "t"}
# x = scores.insert_one(score)


def insertscore(name, score, gameid):
    scoretype = "s"
    if(gameid == 1 or gameid == 3):
        scoretype = "t"
    score = {"name": name, "score": score, "gameid": gameid, "scoretype" : scoretype}
    print("Added score to db")

def readgames():
    gamelist = games.find()
    return gamelist

def getscoreboard(gameid):
    order = -1
    if(gameid == 1):
        order = 1
    query = {"gameid": gameid}
    result = scores.find(query).sort("score", order)
    result = list(result)
    result = dumps(result)
    return result

