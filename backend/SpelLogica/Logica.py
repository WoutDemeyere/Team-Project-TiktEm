from Models.Tik import Tik
import time
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
import random
import os



clear = lambda: os.system('cls')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


def init():
    menu()

def menu():
    tiks = initTiks()
    print(f"Kies een optie in het menu")
    print(f"0: Begin spel")
    print(f"1: List tiks")
    print(f"2: close")
    value = input("Uw keuze: ")
    clear()
    print(f"Kies een speltype in het menu")
    print(f"0: Speedrun")
    print(f"1: Simon Says")

    gametype = int(input("Uw keuze: "))

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
    if gametype == 0:
        speedRun(tiks)
    elif gametype == 1:
        simonSays(tiks)
    
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
    clear()
    while(game == True):
        clear()
        sequence.append(random.randint(0,3))
        for i in sequence:
            turnOn(tiks[i])
            print(f"Tik nr {tiks[i].id} lit up, remember it!")
            time.sleep(1.5)
            turnOff(tiks[i])
            clear()
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

@socketio.on('F2B_start')
def startGame():
    socketio.emit("connected")
    print("test",flush=True)
    menu()


def turnOn(item):
    item.tikstatus = True
    item.lightstatus = True
    item.green = 256
    item.red = 0
    item.blue = 0
    # Send to correct tik via mqtt

def turnOff(item):
    item.tikstatus = False
    item.lightstatus = False
    item.green = 0
    item.red = 0
    item.blue = 0

def awaitTik(item):
    item.tikstatus = True
    item.lightstatus = False
    item.green = 256
    item.red = 0
    item.blue = 0

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
