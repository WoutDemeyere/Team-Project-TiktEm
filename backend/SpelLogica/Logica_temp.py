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
import threading


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
colorhuntscore = 0

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode()
    payload_dict = json.loads(payload)
    tiktem.update_status(payload_dict)

def init():
    menu()

# def menu(data):
#     tiks = initTiks()
#     print(f"Kies een optie in het menu")
#     print(f"0: Begin spel")
#     print(f"1: List tiks")
#     print(f"2: close")
#     value = input("Uw keuze: ")
#     #clear()
#     # print(f"Kies een speltype in het menu")
#     # print(f"0: Speedrun")
#     # print(f"1: Simon Says")

#     gametype = data['gameid'] #int(input("Uw keuze: "))

#     if(value == "0"):
#         initGame(tiks,gametype)
#     elif(value == "1"):
#         listTiks(tiks)

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
        test()
    elif gametype == 2:
        simonSays(tiks)
    elif gametype == 4:
        colorhunt()
    
def speedRun(tiks):
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

def simonSays(tiks):
    game = True
    sequence = []
    #clear()
    while(game == True):
        #clear()
        sequence.append(random.randint(0,3))
        for i in sequence:
            turnOn(tiks[i])
            print(f"Tik nr {tiks[i].id} lit up, remember it!")
            time.sleep(1.5)
            turnOff(tiks[i])
            
            #clear()
        for i in sequence:
            awaitTik(tiks[i])
            value = int(input("Press the next number in the sequence and press enter: "))
            if(value != i):
                game = False
                score = len(sequence)-1
                print(f"Wrong Tik your score was {score}")
                socketio.emit("B2F_score", score,broadcast=True)
                break      
        
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

def test():
    print("STARTING TEST GAME")
    tiktem.reset_tiks()
    tiktem.set_game(0)
    tiktem.update_tiks()

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
        item.turn_on(0, 255, 0)
        tiktem.update_tiks()
        while active == True:
            value = tiktem.get_tik_status(item.id)
            
           
            if value == True:
                print(f"Tik {item.id} has value: {value}")
                active = False
                item.turn_off()
                tiktem.update_tiks()
            # else:
            #     print(f"Stil waiting you twat")
            #time.sleep(0.5)
        
    endtime = datetime.now()
    score = (endtime - starttime).total_seconds()
    print(f"Congratulations you finished the sequence in {score} seconds")
    socketio.emit("B2F_score", score,broadcast=True)


def colorhuntlight(colorhunttype,tikid):
    time.sleep(2)
    if(colorhunttype == 0):
        item.turn_on(255, 0, 0)
        tiktem.update_tiks()
        starttime = datetime.now()
        currenttime = datetime.now()
            while((endtime - starttime).total_seconds() < 3):
                value = tiktem.get_tik_status(tikid)
                if(value==1):
                    item.turn_off()
                    tiktem.update_tiks()
                    colorhuntscore += 10
                    return ""
        #3 seconds rood
    elif(colorhunttype == 1):
        item.turn_on(0, 0, 255)
        tiktem.update_tiks()
        starttime = datetime.now()
        currenttime = datetime.now()
            while((endtime - starttime).total_seconds() < 5):
                value = tiktem.get_tik_status(tikid)
                if(value==1):
                    item.turn_off()
                    tiktem.update_tiks()
                    colorhuntscore += 4
                    return ""
        #5 seconds blauw
    elif(colorhunttype == 2):
        item.turn_on(0, 255, 0)
        tiktem.update_tiks()
        starttime = datetime.now()
        currenttime = datetime.now()
            while((endtime - starttime).total_seconds() < 8):
                value = tiktem.get_tik_status(tikid)
                if(value==1):
                    item.turn_off()
                    tiktem.update_tiks()
                    colorhuntscore += 1
                    return ""
        #8 seconds groen


def colorhunt():
    colorhuntscore = 0
    tiks = tiktem.tiks()
    for item in tiks:
        colortype = random.randint(0,2)
        x = threading.Thread(target=colorhuntlight, args=(colortype,item.id))
        x.start()
    time.sleep(2)
    starttime = datetime.now()
    currenttime = datetime.now()
    while((endtime - starttime).total_seconds() < 60):
        for item in tiks:
            value = tiktem.get_tik_status(item.id)
            if(value==1):
                colortype = random.randint(0,2)
                x = threading.Thread(target=colorhuntlight, args=(colortype,item.id))
    time.sleep(8)
    print(f"Congratulations you finished colorhunt with a score of {colorhuntscore} ")
    socketio.emit("B2F_score", colorhuntscore,broadcast=True)


@socketio.on('F2B_start')
def startGame(data):
    socketio.emit("connected")
    print(data,flush=True)
    gametype = data['gameid']
    initGame(tiks,gametype)
    test()

if __name__ == '__main__':
    mqtt.subscribe('tiktem/tiksout')
    socketio.run(app, debug=False, host='0.0.0.0')


#    "{\"tik_id\": 3, \"tik_status\": true, \"light_status\": true, \"red\": 255, \"green\":255, \"blue\": 255}"
