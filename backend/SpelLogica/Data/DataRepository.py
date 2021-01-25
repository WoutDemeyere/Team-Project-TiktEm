from .Database import Database
class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def readgames():
        sql = 'SELECT * FROM Games'
        params = []
        return Database.get_rows(sql,params)
    
    @staticmethod
    def getscoreboard(gameid):
        if(gameid == 1):
            sql = 'SELECT * FROM Scores where gameid = %s ORDER BY score ASC'
        else: 
            sql = 'SELECT * FROM Scores where gameid = %s ORDER BY score DESC'

        params = [gameid]
        return Database.get_rows(sql,params)

    @staticmethod
    def insertscore(name, score, gameid ):
        sql = 'SELECT * FROM Scores where name = %s AND gameid = %s'
        params = [name,gameid]
        existing = Database.get_rows(sql,params)
        if(len(existing) > 0):
            if(gameid == 1):
                if(score < existing[0]["score"]):
                    sql = 'UPDATE Scores SET score = %s WHERE id = %s'
                    params = [score, existing[0]["id"]]
            else:
                if(score > existing[0]["score"]):
                    sql = 'UPDATE Scores SET score = %s WHERE id = %s'
                    params = [score, existing[0]["id"]]
        else:
            scoretype = "s"
            if(gameid == 1 or gameid == 3):
                scoretype = "t"
            sql = 'INSERT INTO Scores (name, score, gameid, scoretype) VALUES (%s, %s, %s, %s);'
            params = [name, score, gameid, scoretype]
        return Database.execute_sql(sql,params)