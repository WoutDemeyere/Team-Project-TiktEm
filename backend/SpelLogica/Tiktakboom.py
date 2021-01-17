import random
import threading
import time
from Models.TiktEm import TiktEm

timeUltilBoomMIN = 15
timeUltilBoomMAX = 35
game = False
score = 0
maximaleKnipperDelayTikTakBoom = 2

# tijdelijk --------------
value_touch = False
def check_touch():
    global value_touch
    value_touch = bool(input("toets 1 om de touch sensor aan te raken >> "))

def check_game():
    global game
    game = bool(input("toets 'enter' om de game te stoppen >> "))



def TikTakBoomStart():
    global game
    global score

    score = 0
    game = True
    for tik in range(0, 4):
        x = threading.Thread(target=TikTakBoomThread, args=())
        x.start()

    while game == True:
        time.sleep(0.1)
    
    print("DE SCORE IS " + str(score))
    



def TikTakBoomThread():
    global game
    global score
    global timeUltilBoomMAX

    sleepTime = 3

    while game == True:
        # start game
        timeUntilBoom = random.randint(timeUltilBoomMIN, timeUltilBoomMAX)
        gameResult = TikTakBoomLogic(timeUntilBoom, timeUltilBoomMAX)

        if gameResult == "KABAM":
            game = False        # zorgen dat de andere threads stoppen

            # ontplof signaal duidelijk maken
            print("KABAM")
            for x in range(0, 10):
                # show tik blauw met tone 200 -------------------->
                print("blauw")
                time.sleep(0.2)

                # show tik paars met tone 700  ----------------->
                print("paars")
                time.sleep(0.2)

            # show niets -------------->
            print("niets")


        elif gameResult == "AFGETIKT":
            score += 1

            print("goed gedaan jonge")
            # aftik signaal
            # show tik appelblauw met tone 1000 -------------------->
            time.sleep(0.1)
            # show niets ------------>
            print("niets")

            time.sleep(sleepTime)
                

        elif gameResult == "STOP":
            # show tik paars met tone 700 -------------------->
            print("paars")
            time.sleep(0.2)
            # show niets -------------------->
            print("niets")
    
    print("End thread")



def TikTakBoomLogic(timeUntilBoom, timeUltilBoomMAX):
    global game

    global value_touch
    value_touch = False
    # x = threading.Thread(target=check_touch, args=())
    # x.start()

    # y = threading.Thread(target=check_game, args=())
    # y.start()


    timeBoom = float(time.time()) + timeUntilBoom
    timeLeft = timeUntilBoom
    lightActive = False
    knipperDelayTimeAbsoluut = 0
    firstTimeNearEnd = True
    touchWasActivated = False

    while timeLeft > 0 and game == True:
        # read touch sensor  --------------->
        # value_touch = tiktem.get_tik_status(item.id)

        if value_touch == False:

            if timeLeft >= 0.5:
                # checken of hij van knipper status mag veranderen
                if float(time.time()) >= knipperDelayTimeAbsoluut:

                    # de knipper snelheid berekenen
                    timeAbsoluutPercent = 1 - ((timeUltilBoomMAX - timeLeft) / timeUltilBoomMAX)
                    knipperDelayTime = maximaleKnipperDelayTikTakBoom * timeAbsoluutPercent
                    knipperDelayTimeAbsoluut = float(time.time()) + knipperDelayTime
                    
                    timeLeftPercent = timeLeft / timeUntilBoom

                    if lightActive == False:
                        # berekeningen voor de led kleur
                        green = 255 * timeLeftPercent
                        red = 255 - green
                        lightActive = True
                        # licht naar de esp sturen -------------->
                        print(red, green)

                    else:
                        # licht uitzetten esp ----------->
                        print("0")
                        lightActive = False

            # NEAR THE END, LAST CHANSE 0.5S
            elif firstTimeNearEnd == True:
                firstTimeNearEnd = False
                # rood naar de esp sturen ----------->
                print("255", "last")


        # ------------TOUCH SENSOR IS GETIKT ---------------
        else:      
            touchWasActivated = True
            break

        time.sleep(0.01)
        timeLeft = timeBoom - float(time.time())
    # ------------------------ END WHILE LOOP-----------------


    if touchWasActivated == False and game == True:
        # ----------------------------------------------
        # TIME IS OP --> kaboem
        # ------------------------------------------------
        return "KABAM"

    elif touchWasActivated == True and game == True:
        # -----------------------------------------------
        # AFGETIKT
        # -----------------------------------------------
        return "AFGETIKT"

    elif game == False:
        # --------------------------------------------------
        # andere tik is ontploft of player stopt het spel
        # --------------------------------------------------
        return "STOP"


if __name__ == '__main__':
    TikTakBoomStart()
