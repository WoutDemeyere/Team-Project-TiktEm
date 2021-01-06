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
    
    def get_tik_status(tik_id):
        return tiks[tik_id].tik_status

    def update_status(data)
        tiks[data['tik_id']].light_status = data['light_status']
        tiks[data['tik_id']].red = data['red']
        tiks[data['tik_id']].green = data['green']
        tiks[data['tik_id']].blue = data['blue']
    
    def update_tiks(self):
        for i in range(self.amount):
            data = dict(tik_id=tiks[i].id, game_id=self.curr_gameid, tik_status=tiks[i].tikstatus, light_status=tiks[i].light_status, red=tiks[i].red, green=tiks[i].green, blue=tiks[i].blue)
            data_raw = json.dumps(data)
            self.mqtt.publish('tiktem/tiks', data_raw)
    
