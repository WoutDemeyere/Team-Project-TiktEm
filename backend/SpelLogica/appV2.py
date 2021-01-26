#   Custom Models
from Models.Tik import Tik
from Models.TiktEm import TiktEm
from Data.DataRepository import DataRepository

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
import eventlet
#from rich import print


# ------------ CONFIGS ------------
# Flask Config
app = Flask(__name__)
app.config['SECRET_KEY'] = '!superSECRETrealyhardTOGUESS!'

#Fix threading with socketio
eventlet.monkey_patch()

# MQTT Config
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
mqtt = Mqtt(app)

# SocketIO Config
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# TIKS config
amountOfTiks = 4
tiktem = TiktEm(mqtt, amountOfTiks)


# ------------ GAMES ------------
# TIKTAKBOOM
timeUltilBoomMIN = 10
timeUltilBoomMAX = 25
maximaleKnipperDelayTikTakBoom = 1.5

# SPEEDRUN SOLO
sequentie_2_tiks = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
sequentie_3_tiks = [1, 0, 2, 1, 2, 1, 0, 1, 2, 0]
sequentie_4_tiks = [1, 3, 0, 2, 0, 1, 3, 0, 2, 3]

# colorhunt
colorhuntTime = 20

# colorteam
colorTeamTiksDuration = 5


# ----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------ROUTES-----------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------
endpoint = '/tiktem/v1'

@app.route('/')
def hallo():
    return f"Try endpoint {endpoint}"

@app.route(endpoint + '/leaderboard/<game>', methods=['GET'])
def get_leaderboard(game):
    print(game)

    try:
        data = DataRepository.getscoreboard(game)
        return jsonify(data), 200
    except:
        return jsonfiy({'status': 'Er ging iets mis bij het lezen van het leaderboard'}), 500

@app.route(endpoint + '/gameinfo', methods=['GET'])
def get_gameinfo():
    try:
        data = DataRepository.readgames()
        return jsonify(data), 200
    except:
        return jsonfiy({'status': 'Er ging iets mis bij het lezen van de game info'}), 500

@app.route(endpoint + '/startgame', methods=['GET'])
def start_game():
    print("-----------------------\n")

    if tiktem.game_on == True:
        return {'status': 'Er is al een game bezig, gelieve te wachten'}, 500

    game_id = int(request.args.get('gameid'))

    username = request.args.get('username')
    try:
        if game_id < 7:
            if game_id == 1:
                print("- Starting Speedrun -\n")
                print("-----\n")
                x = threading.Thread(target=speedRun, args=(username, game_id))
                x.start()
            elif game_id == 2:
                print("- Starting Simon Says (singleplayer) -\n")
                x = threading.Thread(target=simonSays, args=(username, game_id))
                x.start()
            elif game_id == 3:
                print("- Starting TikTakBoem -\n")
                x = threading.Thread(target=TikTakBoomStart, args=(username, game_id))
                x.start()
            elif game_id == 4:
                print("- Starting Colorhunt (singleplayer) -\n")
                x = threading.Thread(target=colorhunt, args=(username, game_id))
                x.start()
            elif game_id == 5:
                print("- Starting color team")
                x = threading.Thread(target=colorTeam, args=(username, game_id))
                x.start()
            elif game_id == 6:
                print("- Starting Simon Says VS")
                x = threading.Thread(target=simonSaysVS, args=(username, game_id))
                x.start()

            return jsonify({'status': f"Started game {game_id}"}), 200

        else:
            raise ValueError

    except ValueError:
        print(f"><--->< Game id {game_id} is not valid")
        return jsonfiy({'status': 'Onbestaande game ID'}), 500

    except Exception as ex:
        print(f"><--->< Something went wrong : {ex}")
        return jsonfiy({'status': 'Er ging iets mis bij het starten van de game'}), 500

@app.route(endpoint + '/stopgame', methods=['GET'])
def stop_game():
    print("Stopping Game")
    
    try:
        tiktem.game_on = False
        return jsonify({'status': 'OK'}), 200
    except:
        return jsonfiy({'status': 'Er ging iets mis bij het stoppen van de game'}), 500

@app.route(endpoint + '/reset', methods=['GET'])
def reset_tiks():
    print("Reseting tiks")

    try:
        tiktem.reset_tiks()
        return jsonify({'status': 'OK'}), 200
    except:
        return jsonfiy({'status': 'Er ging iets mis bij het resetten van de tiks'}), 500

@app.route(endpoint + '/batteries', methods=['GET'])
def get_battery_levels():
    print("Getting battery levels")
    
    try:
        battery_levels = tiktem.get_batt_levels()
        return jsonify(battery_levels), 200
    except:
        return jsonfiy({'status': 'Er ging iets mis bij het inlezen van de batterij status'}), 500

# ----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------MQTT-------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode()
    payload_dict = json.loads(payload)

    if(message.topic == "tiktem/tiksout"):
        tiktem.update_status(payload_dict)

    elif(message.topic == "tiktem/batt/update"):
        tiktem.update_batt_status(payload_dict)


def mqtt_test():
    while True:
        tiktem.tiks[3].turn_on(255, 0, 0, 0)
        time.sleep(0.3)
        tiktem.tiks[3].turn_off()
        time.sleep(0.3)


# ----------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------GAMES------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------SPEEDRUN-------------------------------------------
def speedRun(username, gameid):
    global sequentie_2_tiks
    global sequentie_3_tiks
    global sequentie_4_tiks

    tiktem.reset_tiks()
    tiktem.score = 0
    tiktem.game_on = True

    starttime = time.time()
    tik_is_up = False
    sequentie_place_counter = 0

    

    # de juiste sequentie ophalen voor het aantal gebruikte tiks
    if tiktem.amount == 2:
        sequentie = sequentie_2_tiks        # NOG ERROR LOGGING INVOEGEN
    elif tiktem.amount == 3:
        sequentie = sequentie_3_tiks
    elif tiktem.amount == 4:
        sequentie = sequentie_4_tiks

    tiks_left = len(sequentie)
    socketio.emit("B2F_speedrun_tiksleft", tiks_left, broadcast=True)

    tik_id = sequentie[sequentie_place_counter]

    while tiktem.game_on == True:
        if tik_is_up == False:
            # de tik 1 keer oplichten
            tik_is_up = True
            tiktem.tiks[tik_id].turn_on(0, 255, 0, 700)
            print(f"-+- Tik {tik_id} has lit up")

        touch_value = tiktem.get_tik_status(tik_id)
        if touch_value == True:
            # tik is getikt signaal uitzetten en de volgende in de sequentie starten
            tiktem.tiks[tik_id].tik_is_touched_signaal()
            sequentie_place_counter += 1
            tik_is_up = False

            tiks_left = tiks_left - 1
            socketio.emit("B2F_speedrun_tiksleft", tiks_left, broadcast=True)

            if sequentie_place_counter == 10:
                # spel is gedaan
                tiktem.score = time.time() - starttime

                DataRepository.insertscore(username, tiktem.score, gameid)
                socketio.emit("B2F_speedrun_ended", tiktem.score, broadcast=True)
                print(f"\n+++++ Congratulations you finished the sequence in {tiktem.score} seconds +++++ \n")         
                break

            tik_id = sequentie[sequentie_place_counter]
        
        time.sleep(0.005)

    tiktem.game_end_sequentie_tiks()            # einde visualiseren


# -------------------------------------------------SIMONSAYS----------------------------------------
def simonSays(username, gameid):
    tiktem.reset_tiks()
    tiktem.game_on = True
    tiktem.score = 0

    sequence = []
    for i in range(0, 2):
        seq = random.randint(0, tiktem.amount-1)
        sequence.append(seq)

    while tiktem.game_on == True:
        seq = random.randint(0, tiktem.amount-1)
        sequence.append(seq)

        for i in sequence:
            if tiktem.game_on == True:
                tiktem.tiks[i].turn_on_delay(0, 0, 255, 500, 500)
                print(f"-+- Tik nr {tiktem.tiks[i].id} lit up, remember it!\n")
                time.sleep(1)
                tiktem.tiks[i].turn_off()
            else:
                break       # game has stopped
            
        socketio.emit("B2F_simonsays_sequence", len(sequence), broadcast=True)

        if tiktem.game_on == True:
            for i in sequence:
                if tiktem.game_on == True:
                    # print(sequence)
                    pressed = False
                    while pressed == False and tiktem.game_on == True:
                        for tik in tiktem.tiks:
                            if tiktem.game_on == True:
                                valueTouch = tiktem.get_tik_status(tik.id)
                                if valueTouch == True:
                                    pressed = True

                                    if tik.id == i:         # JUIST
                                        tik.turn_on_delay(0, 255, 0, 800, 300)
                                        time.sleep(0.6)
                                        tik.turn_off()

                                    elif tik.id != i:       # FOUT
                                        tik.turn_on_delay(255, 0, 0, 200, 500)
                                        tiktem.game_on = False
                                        tiktem.score = len(sequence)-1
                                        if tiktem.score == 2:       # geen punten als je het van de eerste keer fout hebt
                                            tiktem.score = 0
                                        print(f"\n+++++ Wrong Tik your score was {tiktem.score} +++++\n")
                                        DataRepository.insertscore(username, tiktem.score, gameid)
                                        socketio.emit("B2F_simonsays_ended", tiktem.score, broadcast=True)
                                        break  
                            else:
                                break           # game has stopped  
                        time.sleep(0.005)
                else:
                    break                       # game has stopped  
                

# -------------------------------------------------COLORHUNT------------------------------------------
def colorhunt(username, gameid):
    global colorhuntTime

    tiktem.reset_tiks()
    tiktem.game_on = True
    tiktem.score = 0
    tiks = tiktem.tiks

    t_end = time.time() + colorhuntTime

    for tik in tiks:
        colortype = get_color_type()
        x = threading.Thread(target=colorhuntlight, args=(colortype, tik.id))
        x.start()

    while time.time() < t_end and tiktem.game_on == True:
        time.sleep(0.1)

    # tijd is om of spel is gestopt
    tiktem.game_on = False
    tiktem.game_end_sequentie_tiks()

    print(f"\n+++++ Congratulations you finished colorhunt with a score of {tiktem.score} +++++", flush=True)
    DataRepository.insertscore(username, tiktem.score, gameid)
    socketio.emit("B2F_colorhunt_ended", tiktem.score, broadcast=True)


def colorhuntlight(colorhunttype, tikid):
    if colorhunttype == 0:
        # 4 seconds rood
        tiktem.tiks[tikid].turn_on(255, 0, 0, 1000)
        t_end_tik = time.time() + 4
        while time.time() < t_end_tik and tiktem.game_on == True:
            valueTouch = tiktem.get_tik_status(tikid)
            if(valueTouch == True):
                tiktem.score += 3
                socketio.emit("B2F_colorhunt_score", tiktem.score, broadcast=True)
                tiktem.tiks[tikid].tik_is_touched_signaal()
                break
            time.sleep(0.005)

    elif(colorhunttype == 1):
        # 8 seconds blauw
        tiktem.tiks[tikid].turn_on(0, 0, 255, 300)
        t_end_tik = time.time() + 8
        while time.time() < t_end_tik and tiktem.game_on == True:
            valueTouch = tiktem.get_tik_status(tikid)
            if(valueTouch == True):
                tiktem.score += 2
                socketio.emit("B2F_colorhunt_score", tiktem.score, broadcast=True)
                tiktem.tiks[tikid].tik_is_touched_signaal()
                break
            time.sleep(0.005)

    elif(colorhunttype == 2):
        # 30 seconds groen
        tiktem.tiks[tikid].turn_on(0, 255, 0, 0)
        while tiktem.game_on == True:
            valueTouch = tiktem.get_tik_status(tikid)
            if(valueTouch == True):
                tiktem.score += 1
                socketio.emit("B2F_colorhunt_score", tiktem.score, broadcast=True)
                tiktem.tiks[tikid].tik_is_touched_signaal()
                break
            time.sleep(0.005)

    tiktem.tiks[tikid].turn_off()
    time.sleep(3)
    if tiktem.game_on == True:
        # tik opnieuw oplichten
        colortype = get_color_type()
        x = threading.Thread(target=colorhuntlight, args=(colortype, tikid))
        x.start()

def get_color_type():
    random_int = random.randint(0, 7)
    if random_int == 0:
        return 0
    elif random_int == 1 or random_int == 2:
        return 1
    else:
        return 2


# -------------------------------------------------TIKTAKBOOM--------------------------------------
def TikTakBoomStart(username, gameid):
    print(username, gameid)
    tiktem.reset_tiks()
    tiktem.score = 0
    tiktem.game_on = True
    tiks = tiktem.tiks              # alle beschikbare tiks ophalen

    for tik in tiks:                # voor elke tik een thread opstarten
        x = threading.Thread(target=TikTakBoomThread, args=[tik.id])        # vierkante haakjes of ij doe kut
        x.start()

    while tiktem.game_on == True:             # wachten tot de game gedaan is
        time.sleep(0.01)

    tiktem.game_end_sequentie_tiks()            # ze allemaal eens oplichten om de gebruiker te laten weten dat de game gedaan is
    print("DE SCORE IS " + str(tiktem.score))
    DataRepository.insertscore(username, tiktem.score, gameid)
    socketio.emit("B2F_tiktak_ended", tiktem.score, broadcast=True)



def TikTakBoomThread(tikid):
    global timeUltilBoomMAX
    global timeUltilBoomMIN

    sleepTime = 3

    while tiktem.game_on == True:
        # start game
        timeUntilBoom = random.randint(timeUltilBoomMIN, timeUltilBoomMAX)
        gameResult = TikTakBoomLogic(timeUntilBoom, timeUltilBoomMAX, tikid)
        if gameResult == "KABAM":
            tiktem.game_on = False        # zorgen dat de andere threads stoppen

            # ontplof signaal duidelijk maken
            print("KABAM")
            for x in range(0, 10):
                tiktem.tiks[tikid].turn_on(0, 0, 255, 200)
                time.sleep(0.2)

                tiktem.tiks[tikid].turn_on(255, 0, 255, 700)
                time.sleep(0.2)

            tiktem.tiks[tikid].turn_off()

        elif gameResult == "AFGETIKT":
            tiktem.score += 1
            socketio.emit("B2F_tiktak_score", tiktem.score, broadcast=True)
            print("AFGETIKT")
            # aftik signaal
            tiktem.tiks[tikid].tik_is_touched_signaal()
            time.sleep(0.2)
            tiktem.tiks[tikid].turn_off();
            time.sleep(sleepTime)

        elif gameResult == "STOP":
            break



def TikTakBoomLogic(timeUntilBoom, timeUltilBoomMAX, tikid):
    timeBoom = float(time.time()) + timeUntilBoom
    timeLeft = timeUntilBoom
    lightActive = False
    knipperDelayTimeAbsoluut = 0
    firstTimeNearEnd = True
    touchWasActivated = False

    while timeLeft > 0 and tiktem.game_on == True:

        value_touch = tiktem.get_tik_status(tikid)
        if value_touch == False:
            if timeLeft >= 0.5:
                # checken of hij van knipper status mag veranderen
                if float(time.time()) >= knipperDelayTimeAbsoluut:

                    # de knipper snelheid berekenen
                    timeAbsoluutPercent = 1 - (timeUltilBoomMAX - timeLeft) / timeUltilBoomMAX
                    knipperDelayTime = maximaleKnipperDelayTikTakBoom * timeAbsoluutPercent
                    knipperDelayTimeAbsoluut = float(time.time()) + knipperDelayTime
                    timeLeftPercent = timeLeft / timeUntilBoom

                    if lightActive == False:
                        # berekeningen voor de led kleur
                        green = 255 * timeLeftPercent
                        red = 255 - green
                        lightActive = True
                        tiktem.tiks[tikid].turn_on(red, green, 0, 500)

                    else:
                        tiktem.tiks[tikid].turn_off()
                        lightActive = False

            # NEAR THE END, LAST CHANSE 0.5S
            elif firstTimeNearEnd == True:
                firstTimeNearEnd = False
                tiktem.tiks[tikid].turn_on(255, 0, 0, 500)

        # ------------TOUCH SENSOR IS GETIKT ---------------
        else:
            touchWasActivated = True
            break

        time.sleep(0.005)
        timeLeft = timeBoom - float(time.time())
    # ------------------------ END WHILE LOOP-----------------


    if touchWasActivated == False and tiktem.game_on == True:
        # ------------------------------------------------
        # TIME IS OP --> kaboem
        # ------------------------------------------------
        return "KABAM"

    elif touchWasActivated == True and tiktem.game_on == True:
        # -----------------------------------------------
        # AFGETIKT
        # -----------------------------------------------
        return "AFGETIKT"

    elif tiktem.game_on == False:
        # -----------------------------------------------
        # andere tik is ontploft of player stopt het spel
        # -----------------------------------------------
        return "STOP"


# -------------------------------------------------COLORTEAM------------------------------------------
def colorTeam(username, gameid):
    tiktem.reset_tiks()
    tiktem.score_red = 0
    tiktem.score_blue = 0
    tiktem.game_on = True
    
    # first tik for both teams
    tiks = tiktem.tiks              # alle beschikbare tiks ophalen
    x = threading.Thread(target=colorTeamLogic, args=("red", tiks))       # vierkante haakjes want anders wilt threading meerdere argumenten
    x.start()
    y = threading.Thread(target=colorTeamLogic, args=("blue", tiks))
    y.start()

    while(tiktem.game_on == True):
        time.sleep(0.1)
    
    time.sleep(1)
    
    tiktem.game_end_sequentie_tiks()
    
    if tiktem.score_red > tiktem.score_blue:    
        print(f"TEAM ROOD HEEFT GEWONNEN MET ROOD: {tiktem.score_red} TEGEN BLAUW: {tiktem.score_blue}")
        #colorteam_scoredata = {'winner': 'red', 'loser': 'blue', 'score_winner': tiktem.score_red, 'score-loser': tiktem.score_blue}
        socketio.emit("B2F_colorteam_ended", "red", broadcast=True)

    else: 
        #colorteam_scoredata = {'winner': 'blue' , 'loser': 'red', 'score-red': tiktem.score_red, 'score-blue': tiktem.score_blue}
        socketio.emit("B2F_colorteam_ended", "blue", broadcast=True)
        print(f"TEAM BLAUW HEEFT GEWONNEN MET BLAUW: {tiktem.score_blue} TEGEN ROOD: {tiktem.score_blue}")

def colorTeamLogic(teamColor, tiks):
    global colorTeamTiksDuration
                                      
    # elke tik overlopen en kijken of deze al aan staat
    while tiktem.game_on == True:
        random_int = random.randint(0, (tiktem.amount - 1))     # random cijfer genereren
        tik = tiks[random_int]
        in_use = tik.in_use_colorTeam
        if in_use == False:
            # tik is nog niet in gebruik
            used_tik = tik
            used_tik.in_use_colorTeam = True     # tik in gebruik zetten

            if teamColor == "red":
                used_tik.turn_on(255, 0, 0, 300)
            elif teamColor == "blue":
                used_tik.turn_on(0, 0, 255, 600)
            break


    while tiktem.game_on == True: 
        value_touch = tiktem.get_tik_status(used_tik.id)
        if value_touch == True:
            used_tik.tik_is_touched_signaal()

            if teamColor == "red":
                tiktem.score_red += 1
                socketio.emit("B2F_colorteam_score_red", tiktem.score_red, broadcast=True)

                print(f"RED: {tiktem.score_red}")
                if tiktem.score_red == colorTeamTiksDuration:
                    tiktem.game_on = False
                   
                    
                else:
                    # nieuwe tik zoeken om op te lichten
                    x = threading.Thread(target=colorTeamLogic, args=(teamColor, tiks))
                    x.start()
                    break

            elif teamColor == "blue":
                tiktem.score_blue += 1
                socketio.emit("B2F_colorteam_score_blue", tiktem.score_blue, broadcast=True)

                print(f"BLAUW: {tiktem.score_blue}")
                if tiktem.score_blue == colorTeamTiksDuration:
                    tiktem.game_on = False
                    #socketio.emit("B2F_colorteam_ended_winner", "blue", broadcast=True)
                    #socketio.emit("B2F_colorteam_ended_loser", "red", broadcast=True)
                   
                else:
                    # nieuwe tik zoeken om op te lichten
                    x = threading.Thread(target=colorTeamLogic, args=(teamColor, tiks))
                    x.start()
                    break

        time.sleep(0.005)

    time.sleep(0.05)
    tik.in_use_colorTeam = False        # tik weer beschikbaar stellen 

# -------------------------------------------------Simon Says VS------------------------------------------

def simonSaysVS(username, gameid):
    playeramount = 2
    tiktem.reset_tiks()
    tiktem.game_on = True
    tiktem.score = 0
    player = 1
    socketio.emit("B2F_simonsaysvs_player", player, broadcast=True)
    sequence = []
    for i in range(0, 2):
        seq = random.randint(0, tiktem.amount-1)
        sequence.append(seq)

    while tiktem.game_on == True:

        for i in sequence:
            if tiktem.game_on == True:
                tiktem.tiks[i].turn_on_delay(0, 0, 255, 500, 500)
                print(f"-+- Tik nr {tiktem.tiks[i].id} lit up, remember it!\n")
                time.sleep(1)
                tiktem.tiks[i].turn_off()
            else:
                break       # game has stopped

        if tiktem.game_on == True:
            for i in sequence:
                if tiktem.game_on == True:
                    # print(sequence)
                    pressed = False
                    while pressed == False and tiktem.game_on == True:
                        for tik in tiktem.tiks:
                            if tiktem.game_on == True:
                                valueTouch = tiktem.get_tik_status(tik.id)
                                if valueTouch == True:
                                    pressed = True
                                    print("PRESSED")

                                    if tik.id == i:         # JUIST
                                        tik.turn_on(0, 255, 0, 800)
                                        time.sleep(0.6)
                                        tik.turn_off()
                                        

                                    elif tik.id != i:       # FOUT
                                        tik.turn_on_delay(255, 0, 0, 200, 500)
                                        tiktem.game_on = False
                                        print(f"\n+++++ Wrong Tik player {player} lost +++++\n")
                                        if player == 1:
                                            socketio.emit("B2F_simonsaysvs_ended", player+1, broadcast=True)
                                        elif player == 2:
                                            socketio.emit("B2F_simonsaysvs_ended", player-1, broadcast=True)
                                        break  
                            else:
                                break           # game has stopped  
                        time.sleep(0.005)
                else:
                    break                       # game has stopped  
            
            if tiktem.game_on == True:
                waiting = True
                while waiting:
                    for tik in tiktem.tiks:
                        if tiktem.get_tik_status(tik.id) == True:
                            print('ADDED NEW tik to sequence')
                            tik.turn_on(0,0,255, 800)
                            time.sleep(0.4)
                            tik.turn_off()
                            sequence.append(tik.id)
                            waiting = False
                        time.sleep(0.1)
                    time.sleep(0.1)
            
            if player == playeramount:
                player = 1
                socketio.emit("B2F_simonsaysvs_player", player, broadcast=True)
            else:
                player +=1
                socketio.emit("B2F_simonsaysvs_player", player, broadcast=True)






if __name__ == '__main__':
    mqtt.subscribe('tiktem/tiksout')
    mqtt.subscribe('tiktem/batt/update')
    # tiktem.reset_tiks()
    #mqtt_test()
    with app.app_context():
        socketio.run(app, debug=False, host='0.0.0.0', port=5000)
    # socketio.run(app, debug=False, host='0.0.0.0', port=5000)
