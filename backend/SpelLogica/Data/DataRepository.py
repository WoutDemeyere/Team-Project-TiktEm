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
        scoretype = "s"
        if(gameid == 1 or gameid == 3):
            scoretype = "t"
        sql = 'INSERT INTO Scores (name, score, gameid, scoretype) VALUES (%s, %s, %s, %s);'
        params = [name, score, gameid, scoretype]
        return Database.execute_sql(sql,params)