class TiktEm: 
    def __init__(mqtt_client, amount)
        self.mqtt = mqtt_client
        self.amount = amount
        self.tiks = []
        self.reset_tiks()
        self.curr_gameid
    
    def reset_tiks(self):
        for i in range(self.amount):
            tik = Tik(i,False,False,256,256,256)
            self.tiks.append(tik)
    
    def set_game(self, game_id):
        self.curr_gameid = game_id
        if game_id = '0':
            self.reset_tiks()
            self.tiks[0].turn_on(0,255,0)
            self.tiks[1].turn_off()
            self.tiks[2].turn_off()
            self.tiks[3].turn_off()
        elif game_id = '1':
            pass
        elif game_id = '2':
            pass
        elif game_id = '3':
            pass
        elif game_id = '1':
            pass
        elif game_id = '1':
            pass
    
    def update_tiks(self):
        for i in range(self.amount):
            data = dict(tik_id=i.id, game_id=self.curr_gameid, tik_status=i.tikstatus, light_status=i.light_status, red=i.red, green=i.green, blue=i.blue)
            self.mqtt.publish('tiktem/tiks')
    
