#   Custom Models
from Models.Tik import Tik
from Models.TiktEm import TiktEm

#   Flask Imports
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
from flask_cors import CORS

#   Other Imports
from datetime import datetime
import time
import random
import os
import json
import threading
import sys
#from rich import print

#   Flask Config
app = Flask(__name__)
app.config['SECRET_KEY'] = '!superSECRETrealyhardTOGUESS!'

#   MQTT Config
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
mqtt = Mqtt(app)

#   SocketIO Config
socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app)

endpoint = '/tiktem/v1'

tiktem = TiktEm(mqtt, 2)

@app.route('/')
def hallo():
    return f"Try endpoint {endpoint}"

@app.route(endpoint + '/startgame', methods=['GET'])
def start_game():
    print("-----------------------\n")

    game_id = int(request.args.get('gameid'))

    try:
        if game_id < 7:
            if game_id == 1:
                print("- Starting Speedrun -\n")
                print("-----\n")
                speedRun() 
            elif game_id == 2:
                print("- Starting Simon Says (singleplayer) -\n")
                simonSays()
            elif game_id == 3:
                print("- Starting TikTakBoem -\n")
                pass
            elif game_id == 4:
                print("- Starting Colorhunt (singleplayer) -\n")
                colorhunt()
            elif game_id == 5:
                pass
            elif game_id == 6:
                pass

            return jsonify(f"Started game {game_id}"),200

        else:
            raise ValueError

    except ValueError as er:
        print(f"><--->< Game id {game_id} is not valid")
        return jsonify(f"Wrong game id: {game_id}"),400
    
    except Exception as ex:
        print(f"><--->< Something went wrong : {ex}")
        return jsonify(f"Something went wrong"),500
    
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode()
    payload_dict = json.loads(payload)
    tiktem.update_status(payload_dict)

def speedRun():
    tiktem.reset_tiks()

    starttime = datetime.now()
    for item in tiktem.tiks:
        active = True
        print(f"-+- Tik {item.id} has lit up")  
        item.turn_on(0, 255, 0, 800)

        while active == True:
            value = tiktem.get_tik_status(item.id)
            if value == True:
                active = False
                item.turn_off()
        
    endtime = datetime.now()
    score = (endtime - starttime).total_seconds()
    print(f"\n+++++ Congratulations you finished the sequence in {score} seconds +++++ \n")
    socketio.emit("B2F_score", score,broadcast=True)

def simonSays():
    tiktem.reset_tiks()

    game = True
    sequence = []
    while(game == True):
        seq = random.randint(0, tiktem.amount-1)
        sequence.append(seq)
        pressed_tik = 0
        
        for i in sequence:       
            tiktem.tiks[i].turn_on(0, 255, 0, 500)
            print(f"-+- Tik nr {tiktem.tiks[i].id} lit up, remember it!\n")
            time.sleep(0.5)
            tiktem.tiks[i].turn_off()
            time.sleep(0.4)
            
        for i in sequence:
            #print(sequence)
            pressed = False
            while pressed == False:
                for tik in tiktem.tiks:
                    if tiktem.get_tik_status(tik.id) == True:
                        pressed = True

                        if tik.id == i:
                            tik.turn_on(0,0,255, 800)
                            time.sleep(0.5)
                            tik.turn_off()
                            time.sleep(0.5)

                        elif tik.id != i:
                            tik.turn_on(255,0,0, 300)
                            time.sleep(0.5)
                            tik.turn_off()
                            time.sleep(0.5)

                            game = False
                            score = len(sequence)-1
                            print(f"\n+++++ Wrong Tik your score was {score} +++++\n")
                            socketio.emit("B2F_score", score,broadcast=True)
                            break    

def colorhunt():
    tiktem.reset_tiks()
    tiktem.colorhunt_score = 0

    tiks = tiktem.tiks

    for item in tiks:
        colortype = random.randint(0,2)
        x = threading.Thread(target=colorhuntlight, args=(colortype,item.id))
        x.start()

    time.sleep(1)

    t_end = time.time() + 25
    while time.time() < t_end:
        for item in tiks:
            value = tiktem.get_tik_status(item.id)
            if(value==True):
                item.turn_off()
                colortype = random.randint(0,2)
                x = threading.Thread(target=colorhuntlight, args=(colortype,item.id))
                x.start()

    time.sleep(1)
    print(f"\n+++++ Congratulations you finished colorhunt with a score of {tiktem.colorhunt_score} +++++", flush=True)
    socketio.emit("B2F_score", tiktem.colorhunt_score, broadcast=True)

def colorhuntlight(colorhunttype, tikid):
    tiktem.tiks[tikid].turn_off()
    time.sleep(0.5)

    if(colorhunttype == 0):
        tiktem.tiks[tikid].turn_on(255, 0, 0, 800)

        #3 seconds rood
        t_end = time.time() + 3
        while time.time() < t_end:
            value = tiktem.get_tik_status(tikid)
            if(value==True):
                tiktem.colorhunt_score += 4
                break

        tiktem.tiks[tikid].turn_off()
        tiktem.tiks[tikid].tikstatus = True
        print("KILLED THREAD", flush=True)
        sys.exit()
        
    elif(colorhunttype == 1):
        tiktem.tiks[tikid].turn_on(0, 0, 255, 800)

        #5 seconds blauw
        t_end = time.time() + 5
        while time.time() < t_end:
            value = tiktem.get_tik_status(tikid)
            if(value==True):
                tiktem.colorhunt_score += 4
                break

        tiktem.tiks[tikid].turn_off()
        tiktem.tiks[tikid].tikstatus = True
        print("KILLED THREAD", flush=True)
        sys.exit()
        
    elif(colorhunttype == 2):
        tiktem.tiks[tikid].turn_on(0, 255, 0, 800)

        #8 seconds groen
        t_end = time.time() + 8  
        while time.time() < t_end:
            value = tiktem.get_tik_status(tikid)
            if(value==True):
                tiktem.colorhunt_score += 4
                break

        tiktem.tiks[tikid].turn_off()
        tiktem.tiks[tikid].tikstatus = True
        print("KILLED THREAD", flush=True)
        sys.exit()

# TEST
def mqqt_test():
    while True:
        tiktem.tiks[0].turn_on(255, 255, 255, 500)
        time.sleep(0.05)
        tiktem.tiks[0].turn_off()
        time.sleep(0.05)

if __name__ == '__main__':
    mqtt.subscribe('tiktem/tiksout')
    mqqt_test()
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)
    