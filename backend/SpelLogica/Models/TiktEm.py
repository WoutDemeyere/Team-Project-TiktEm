from .Tik import Tik

class TiktEm: 
    def __init__(self, mqtt_client, amount):
        self.mqtt = mqtt_client
        self.amount = amount
        self.tiks = []
        self.init_tiks()
        self.curr_gameid = 0
    
    def init_tiks(self):
        for i in range(self.amount):
            tik = Tik(i,False,False,256,256,256)
            self.tiks.append(tik)
    def reset_tiks(self):
        for tik in self.tiks:
            tik.turn_off()
    
    def set_game(self, game_id):
        self.curr_gameid = game_id
        if game_id == '0':
            self.reset_tiks()
            self.tiks[0].turn_on(0,255,0)
            self.tiks[1].turn_off()
            self.tiks[2].turn_off()
            self.tiks[3].turn_off()
        elif game_id == '1':
            pass
        elif game_id == '2':
            pass
        elif game_id == '3':
            pass
        elif game_id == '1':
            pass
        elif game_id == '1':
            pass
    
    def get_tik_status(self, tik_id):
        return self.tiks[tik_id].tikstatus

    def update_status(self, data):
        #print(f'updated tik {data['tik_id']} {data['light_status']}')
        print(f'UPDATED TIK {data}', flush=True)
        self.tiks[data['tik_id']].tikstatus = data['tik_status']
        self.tiks[data['tik_id']].lightstatus = data['light_status']
        self.tiks[data['tik_id']].red = data['red']
        self.tiks[data['tik_id']].green = data['green']
        self.tiks[data['tik_id']].blue = data['blue']
    
    def update_tiks(self):
        for i in range(self.amount):
            data = dict(tik_id=tiks[i].id, game_id=self.curr_gameid, tik_status=tiks[i].tikstatus, light_status=tiks[i].lightstatus, red=tiks[i].red, green=tiks[i].green, blue=tiks[i].blue)
            data_raw = json.dumps(data)
            self.mqtt.publish(f'tiktem/tiks', data_raw)
    
