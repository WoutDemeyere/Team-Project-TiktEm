from .Tik import Tik
import json
import time

class TiktEm: 
    def __init__(self, mqtt_client, amount):
        self.mqtt = mqtt_client
        self.amount = amount
        self.tiks = []
        self.init_tiks()
        self.curr_gameid = 0
        self.colorhunt_score = 0

        self.color_team1 = False
        self.color_team2 = False

        self.colorteams=[{"color":"blue","sequence":0,"team":1},{"color":"red","sequence":0,"team":2}]

        self.winner=""
    
    def init_tiks(self):
        for i in range(0, self.amount):
            tik = Tik(i,False,False,256,256,256,0, self.mqtt)
            self.tiks.append(tik)

    def reset_tiks(self):
        for tik in self.tiks:
            tik.turn_off()
    
    def get_tik_status(self, tik_id):
        return self.tiks[tik_id].tikstatus
    
    def get_colorhunt_status(self, tik_id):
        return self.tiks[tik_id].colorhunt_status

    def update_status(self, data):
        self.tiks[data['tik_id']].tikstatus = data['tik_status']
        self.tiks[data['tik_id']].lightstatus = data['light_status']
    
