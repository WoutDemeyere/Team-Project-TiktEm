from Models.Tik import Tik
from Models.TiktEm import TiktEm
import time
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
from flask_cors import CORS
import random
import os
import json


#clear = lambda: os.system('cls')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
mqtt = Mqtt(app)

tiktem = TiktEm(mqtt, 2)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode()
    payload_dict = json.loads(payload)
    tiktem.update_status(payload_dict)

def init():
    menu()

def menu(data):
    tiks = initTiks()
    print(f"Kies een optie in het menu")
    print(f"0: Begin spel")
    print(f"1: List tiks")
    print(f"2: close")
    value = input("Uw keuze: ")
    #clear()
    # print(f"Kies een speltype in het menu")
    # print(f"0: Speedrun")
    # print(f"1: Simon Says")

    gametype = data['gameid'] #int(input("Uw keuze: "))

    if(value == "0"):
        initGame(tiks,gametype)
    elif(value == "1"):
        listTiks(tiks)

def initTiks():
    tiks = []
    tik1 = Tik(0,False,False,256,256,256)
    tik2 = Tik(1,False,False,256,256,256)
    tik3 = Tik(2,False,False,256,256,256)
    tik4 = Tik(3,False,False,256,256,256)
    tiks.append(tik1)
    tiks.append(tik2)
    tiks.append(tik3)
    tiks.append(tik4)
    return tiks

def listTiks(tiks):
    for item in tiks:
        print(f"Id: {item.id}")
        print(f"Status: {item.tikstatus}")
        print(f"")

def initGame(tiks,gametype):
    print(f"Game starting")
    time.sleep(1)
    print(f"3..")
    time.sleep(1)
    print(f"2..")
    time.sleep(1)
    print(f"1..")
    time.sleep(1)
    print(f"Start")
    if gametype == 1:
        speedRun(tiks)
    elif gametype == 2:
        simonSays(tiks)
    
# def speedRun(tiks):
    starttime = datetime.now()
    for item in tiks:
        active = True
        while(active == True):
            turnOn(item)
            print(f"Tik {item.id} lit up, press it!")
            # Input here changed to input through mqtt when set up
            value = int(input("Input: "))
            if(value == item.id):
                active = False
            else:
                print(f"Wrong input try again")
    endtime = datetime.now()
    score = (endtime - starttime).total_seconds()
    print(f"Congratulations you finished the sequence in {score} seconds")
    socketio.emit("B2F_score", score,broadcast=True)

# def simonSays(tiks):
#     game = True
#     sequence = []
#     #clear()
#     while(game == True):
#         #clear()
#         sequence.append(random.randint(0,3))
#         for i in sequence:
#             turnOn(tiks[i])
#             print(f"Tik nr {tiks[i].id} lit up, remember it!")
#             time.sleep(1.5)
#             turnOff(tiks[i])
            
#             #clear()
#         for i in sequence:
#             awaitTik(tiks[i])
#             value = int(input("Press the next number in the sequence and press enter: "))
#             if(value != i):
#                 game = False
#                 score = len(sequence)-1
#                 print(f"Wrong Tik your score was {score}")
#                 socketio.emit("B2F_score", score,broadcast=True)
#                 break      
        




@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

def simonSays():
    tiktem.reset_tiks()
    tiktem.set_game(1)
    #tiktem.update_tiks()

    
    game = True
    sequence = []
    while(game == True):
        sequence.append(random.randint(0,1))
        pressed_tik = 0
        
        for i in sequence:
            tiktem.tiks[i].turn_on(0, 255, 0, 500)
            #print(f"Tik nr {tiktem.tiks[i].id} lit up, remember it!")
            time.sleep(1)
            tiktem.tiks[i].turn_off()
            #tiktem.update_tiks()
            
        for i in sequence:
            print(sequence)
            #awaitTik(tiks[i])
            #value = int(input("Press the next number in the sequence and press enter: "))
            #value = tiktem.get_tik_status(i)
            pressed = False
            while pressed == False:
                for tik in tiktem.tiks:
                    if tiktem.get_tik_status(tik.id) == True:
                        pressed = True

                        if tik.id == i:
                            tik.turn_on(0,0,255, 800)
                            time.sleep(0.4)
                            tik.turn_off()
                            time.sleep(1)

                        elif tik.id != i:
                            tik.turn_on(255,0,0, 300)
                            time.sleep(0.4)
                            tik.turn_off()

                            game = False
                            score = len(sequence)-1
                            print(f"Wrong Tik your score was {score}")
                            socketio.emit("B2F_score", score,broadcast=True)
                            break    
                    
                  


def speedRun():
    print("STARTING TEST GAME")
    tiktem.reset_tiks()
    tiktem.set_game(0)
    #tiktem.update_tiks()

    # curr_tik_status = tiktem.get_tik_status(0)
    # while curr_tik_status == False:
    #     print('TIK IS NOT PRESSED')
    #     curr_tik_status = tiktem.get_tik_status(0)
    #     print(tiktem.get_tik_status(0))
    #     time.sleep(0.5)
    
    # print('TIK IS PRESSED')

    starttime = datetime.now()

    for item in tiktem.tiks:
        active = True
        print(f"Tik {item.id} has lit up")  
        item.turn_on(0, 255, 0, 800)
        #tiktem.update_tiks()
        while active == True:
            value = tiktem.get_tik_status(item.id)
            if value == True:
                print(f"Tik {item.id} has value: {value}")
                active = False
                item.turn_off()
                #tiktem.update_tiks()
            # else:
            #     print(f"Stil waiting you twat")
            #time.sleep(0.5)
        
    endtime = datetime.now()
    score = (endtime - starttime).total_seconds()
    print(f"Congratulations you finished the sequence in {score} seconds")
    socketio.emit("B2F_score", score,broadcast=True)

@socketio.on('F2B_start')
def startGame(data):
    socketio.emit("connected")
    print(data,flush=True)

    if data['gameid'] == 1:
        speedRun()
    elif data['gameid'] == 2:
        simonSays()

if __name__ == '__main__':
    mqtt.subscribe('tiktem/tiksout')
    socketio.run(app, debug=False, host='0.0.0.0')


#    "{\"tik_id\": 3, \"tik_status\": true, \"light_status\": true, \"red\": 255, \"green\":255, \"blue\": 255}"
