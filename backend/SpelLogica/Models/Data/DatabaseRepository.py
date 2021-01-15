from pymongo import MongoClient
from bson.json_util import dumps
import pymongo
client = MongoClient('mongodb+srv://klaas:root@clusterteamproject.y22lv.mongodb.net/test')
mydb = client["TeamProjectTiktem"]
games = mydb["Games"]
scores = mydb["Scores"]
class DatabaseRepository:

    @staticmethod
    def insertscore(name, score, gameid):
        scoretype = "s"
        if(gameid == 1 or gameid == 3):
            scoretype = "t"
        score = {"name": name, "score": score, "gameid": gameid, "scoretype" : scoretype}
        print("Added score to db")

    @staticmethod
    def readgames():
        result = games.find()
        result = list(result)
        result = dumps(result)
        return gamelist

    @staticmethod
    def getscoreboard(gameid):
        order = -1
        if(gameid == 1):
            order = 1
        query = {"gameid": gameid}
        result = scores.find(query).sort("score", order)
        result = list(result)
        result = dumps(result)
        return result

