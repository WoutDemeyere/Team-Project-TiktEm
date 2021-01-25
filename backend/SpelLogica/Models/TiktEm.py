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
        self.game_on = False
        self._score = 0        

        # color team zooi
        self.score_red = 0
        self.score_blue = 0

    @property
    def score(self):
        """The score property."""
        return self._score
    @score.setter
    def score(self, value):
        self._score = round(value, 2)
    
    def init_tiks(self):
        for i in range(0, self.amount):
            tik = Tik(i,False,256,256,256,0, self.mqtt)
            self.tiks.append(tik)

    def reset_tiks(self):
        for tik in self.tiks:
            tik.turn_off()

    def game_end_sequentie_tiks(self):
        for tik in self.tiks:
            tik.turn_on_delay(255, 0, 255, 200, 200)
    
    def get_tik_status(self, tik_id):
        tik_status_now = self.tiks[tik_id].tikstatus
        if tik_status_now == True:
            self.tiks[tik_id].tikstatus = False
        return tik_status_now

    def update_status(self, data):
        self.tiks[data['tik_id']].tikstatus = data['tik_status']

    def get_batt_levels(self):
        self.mqtt.publish('tiktem/batt/status', '{"thing": "hello"}') #Trigger battery send on tik

        time.sleep(1.5)
        batt_levels = []
        for tik in self.tiks:
            batt_levels.append({'id': tik.id, 'batt_level': tik.batt_level})
        return batt_levels


    def update_batt_status(self, data):
        print(f"UPDATED BATT LEVEL: {data}")
        self.tiks[data['tik_id']].batt_level = data['batt_status']
