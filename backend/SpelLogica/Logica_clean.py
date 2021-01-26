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

# ------------ GAMES ------------
# TIKTAKBOOM
timeUltilBoomMIN = 15
timeUltilBoomMAX = 35
game = False
score = 0
maximaleKnipperDelayTikTakBoom = 2


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


# ----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------ROUTES-----------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------
global1=0
global2=0
winner=""
stop=0

@app.route('/')
def hallo():
    return f"Try endpoint {endpoint}"

@app.route(endpoint + '/leaderboard/<game>', methods=['GET'])
def get_leaderboard(game):
    data = DataRepository.getscoreboard(game)
    return jsonify(data), 200

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
                print("starting color team")
                colorteam()
            elif game_id == 6:
                pass

            return jsonify(f"Started game {game_id}"),200

        else:
            raise ValueError

    except ValueError as er:
        print(f"><--->< Game id {game_id} is not valid")
        return jsonify(f"Wrong game id: {game_id}"), 400

    except Exception as ex:
        print(f"><--->< Something went wrong : {ex}")
        return jsonify(f"Something went wrong"), 500


# ----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------MQTT-------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode()
    payload_dict = json.loads(payload)
    tiktem.update_status(payload_dict)


def mqtt_test():
    while True:
        tiktem.tiks[0].turn_on(255, 255, 255, 500)
        time.sleep(0.05)
        tiktem.tiks[0].turn_off()
        time.sleep(0.05)


# ----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------GAMES------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------SPEEDRUN----------------------------------------
def speedRun():
    tiktem.reset_tiks()

    tiks_left = tiktem.amount
    socketio.emit("B2F_speedrun_tiksleft", tiks_left, broadcast=True)

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
    socketio.emit("B2F_speedrun_ended", score,broadcast=True)

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
            # print(sequence)
            pressed = False
            while pressed == False:
                for tik in tiktem.tiks:
                    if tiktem.get_tik_status(tik.id) == True:
                        pressed = True

                        if tik.id == i:
                            tik.turn_on(0, 0, 255, 800)
                            time.sleep(0.5)
                            tik.turn_off()
                            time.sleep(0.5)

                        elif tik.id != i:
                            tik.turn_on(255, 0, 0, 300)
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
        colortype = random.randint(0, 2)
        x = threading.Thread(target=colorhuntlight, args=(colortype, item.id))
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

def colorhuntlight(colorhunttype,tikid):
    tiktem.tiks[tikid].turn_off()
    time.sleep(0.5)

    if(colorhunttype == 0):
        tiktem.tiks[tikid].turn_on(255, 0, 0, 800)

        # 3 seconds rood
        t_end = time.time() + 3
        while time.time() < t_end:
            value = tiktem.get_tik_status(tikid)
            if(value == True):
                tiktem.colorhunt_score += 4
                break

        tiktem.tiks[tikid].turn_off()
        tiktem.tiks[tikid].tikstatus = True
        print("KILLED THREAD", flush=True)
        sys.exit()

    elif(colorhunttype == 1):
        tiktem.tiks[tikid].turn_on(0, 0, 255, 800)

        # 5 seconds blauw
        t_end = time.time() + 5
        while time.time() < t_end:
            value = tiktem.get_tik_status(tikid)
            if(value == True):
                tiktem.colorhunt_score += 4
                break

        tiktem.tiks[tikid].turn_off()
        tiktem.tiks[tikid].tikstatus = True
        print("KILLED THREAD", flush=True)
        sys.exit()

    elif(colorhunttype == 2):
        tiktem.tiks[tikid].turn_on(0, 255, 0, 800)

        # 8 seconds groen
        t_end = time.time() + 8
        while time.time() < t_end:
            value = tiktem.get_tik_status(tikid)
            if(value == True):
                tiktem.colorhunt_score += 4
                break

        tiktem.tiks[tikid].turn_off()
        tiktem.tiks[tikid].tikstatus = True
        print("KILLED THREAD", flush=True)
        sys.exit()


# -------------------------------------------------TIKTAKBOOM--------------------------------------
def TikTakBoomStart():
    global timeUltilBoomMAX

    tiktem.reset_tiks()
    tiktem.TikTakBoom_score = 0
    tiktem.game = True

    tiks = tiktem.tiks              # alle beschikbare tiks ophalen

    for tik in tiks:                # voor elke tik een thread opstarten
        x = threading.Thread(target=TikTakBoomThread,
                             args=(tik.id, timeUltilBoomMAX))
        x.start()

    while tiktem.game == True:             # wachten tot de game gedaan is
        time.sleep(0.1)

    print("DE SCORE IS " + str(tiktem.TikTakBoom_score))
    socketio.emit("B2F_score", tiktem.TikTakBoom_score, broadcast=True)


def TikTakBoomThread(tikid, timeUltilBoomMAX):
    sleepTime = 3

    while tiktem.game == True:
        # start game
        timeUntilBoom = random.randint(timeUltilBoomMIN, timeUltilBoomMAX)
        gameResult = TikTakBoomLogic(timeUntilBoom, timeUltilBoomMAX, tikid)

        if gameResult == "KABAM":
            tiktem.game = False        # zorgen dat de andere threads stoppen

            # ontplof signaal duidelijk maken
            print("KABAM")
            for x in range(0, 10):
                # show tik blauw met tone 200 -------------------->
                tiktem.tiks[tikid].turn_on(0, 0, 255, 200)
                print("blauw")
                time.sleep(0.2)

                # show tik paars met tone 700  ----------------->
                tiktem.tiks[tikid].turn_on(255, 0, 255, 700)
                print("paars")
                time.sleep(0.2)

            # show niets -------------->
            tiktem.tiks[tikid].turn_off()
            print("niets")

        elif gameResult == "AFGETIKT":
            tiktem.TikTakBoom_score += 1

            print("goed gedaan jonge")
            # aftik signaal
            # show tik appelblauw met tone 1000 -------------------->
            tiktem.tiks[tikid].turn_on(0, 255, 255, 1000)
            time.sleep(0.1)
            # show niets ------------>
            tiktem.tiks[tikid].turn_off()
            print("niets")

            time.sleep(sleepTime)

        elif gameResult == "STOP":
            # show tik paars met tone 700 -------------------->
            tiktem.tiks[tikid].turn_on(255, 0, 255, 700)
            print("paars")
            time.sleep(0.2)
            # show niets -------------------->
            tiktem.tiks[tikid].turn_off()
            print("niets")

    print("End thread")


def TikTakBoomLogic(timeUntilBoom, timeUltilBoomMAX, tikid):
    timeBoom = float(time.time()) + timeUntilBoom
    timeLeft = timeUntilBoom
    lightActive = False
    knipperDelayTimeAbsoluut = 0
    firstTimeNearEnd = True
    touchWasActivated = False

    while timeLeft > 0 and tiktem.game == True:
        # read touch sensor  --------------->
        value_touch = tiktem.get_tik_status(tikid)

        if value_touch == False:

            if timeLeft >= 0.5:
                # checken of hij van knipper status mag veranderen
                if float(time.time()) >= knipperDelayTimeAbsoluut:

                    # de knipper snelheid berekenen
                    timeAbsoluutPercent = 1 - \
                        ((timeUltilBoomMAX - timeLeft) / timeUltilBoomMAX)
                    knipperDelayTime = maximaleKnipperDelayTikTakBoom * timeAbsoluutPercent
                    knipperDelayTimeAbsoluut = float(
                        time.time()) + knipperDelayTime

                    timeLeftPercent = timeLeft / timeUntilBoom

                    if lightActive == False:
                        # berekeningen voor de led kleur
                        green = 255 * timeLeftPercent
                        red = 255 - green
                        lightActive = True
                        # licht naar de esp sturen -------------->
                        tiktem.tiks[tikid].turn_on(red, green, 0, 500)
                        print(red, green)

                    else:
                        # licht uitzetten esp ----------->
                        tiktem.tiks[tikid].turn_off()
                        print("0")
                        lightActive = False

            # NEAR THE END, LAST CHANSE 0.5S
            elif firstTimeNearEnd == True:
                firstTimeNearEnd = False
                # rood naar de esp sturen ----------->
                tiktem.tiks[tikid].turn_on(255, 0, 0, 500)
                print("255", "last")

        # ------------TOUCH SENSOR IS GETIKT ---------------
        else:
            touchWasActivated = True
            break

        time.sleep(0.01)
        timeLeft = timeBoom - float(time.time())
    # ------------------------ END WHILE LOOP-----------------

    if touchWasActivated == False and tiktem.game == True:
        # ----------------------------------------------
        # TIME IS OP --> kaboem
        # ------------------------------------------------
        return "KABAM"

    elif touchWasActivated == True and tiktem.game == True:
        # -----------------------------------------------
        # AFGETIKT
        # -----------------------------------------------
        return "AFGETIKT"

    elif tiktem.game == False:
        # --------------------------------------------------
        # andere tik is ontploft of player stopt het spel
        # --------------------------------------------------
        return "STOP"


# -------------------------------------------------COLORTEAM--------------------------------------
def colorteam():
    tiktem.reset_tiks()
    #TiktEm.reset_tiks()
    #2 teams
    
    #firtst button of sequence of both teams
    x = threading.Thread(target=colorteamCheck, args=("red", 0, 1))
    x.start()

    y = threading.Thread(target=colorteamCheck, args=("red", 0, 1))
    y.start()



    while(stop==0):
        #get from frontend stop=1 get from route
        if(tiktem.color_team1):
            tiktem.color_team1 = False
            tiktem.colorteams[0]["sequence"] +=1
            print(f"team2 have pushed the {tiktem.colorteams[0]['sequence']}e button")
            global1=0
            # x = threading.Thread(target=colorteamCheck, args=(team[0]))
            x = threading.Thread(target=colorteamCheck, args=("red", 0, 1))
            x.start()

        if(tiktem.color_team2):
            tiktem.color_team2 = False
            tiktem.colorteams[1]["sequence"]+=1
            print(f"team2 have pushed the {tiktem.colorteams[1]['sequence']}e button")
            global2=0
            y = threading.Thread(target=colorteamCheck, args=("blue", 0, 2))
            y.start()

        #kan ook in for loop
        if(tiktem.colorteams[0]["sequence"]==10):
            print(f"team {tiktem.colorteams[0]['color']} has won")
            winner=tiktem.colorteams[0]['color']
            break
        elif(tiktem.colorteams[1]["sequence"]==10):
            print(f"team {tiktem.colorteams[1]['color']} has won")
            winner=tiktem.colorteams[1]['color']
            break

def colorteamCheck(color,sequence,team):
    print(tiktem.colorteams)
    openTiks=[]
    #checking wich tik available
    for tik in tiktem.tiks:

        lightstatus=tik.lightstatus
        #print(tik)
        if(lightstatus==False):
            openTiks.append(tik)

    #print(openTiks, flush=True)

    #select possible tik
    selection=random.randint(0, len(openTiks)-1)

    #light up selected light
    active=True


    r=0
    g=0
    b=0

    if(tiktem.colorteams[0]['color']=="red"):
        r=255
    elif(tiktem.colorteams[0]['color']=="green"):
        g=255
    elif(tiktem.colorteams[0]['color']=="blue"):
        b=255

    openTiks[selection].turn_on(r, g, b, 500)
    #check if selected light gets pushed
    
    while active == True:
        #checking push status of selected tik
        value = tiktem.get_tik_status(openTiks[selection].id)
        if value == True:
            active = False
            openTiks[selection].turn_off()
            #checking what team this tik belongs to
            if(tiktem.colorteams[0]["team"]==1):
                tiktem.color_team1 = True
                
            elif(tiktem.colorteams[0]["team"]==2):
                tiktem.color_team2 = True
            
            print(tiktem.colorteams)
            print(tiktem.color_team1, tiktem.color_team2)
            
            sys.exit()



if __name__ == '__main__':
    mqtt.subscribe('tiktem/tiksout')
    #mqtt_test()
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)
