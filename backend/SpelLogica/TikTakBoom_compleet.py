import threading
import time

game = False
maximaleKnipperDelayTikTakBoom = 2
timeUntilBoom = 20
timeUltilBoomMAX = 40

value_touch = False

def check_touch():
    global value_touch
    value_touch = bool(input("toets 1 om de touch sensor aan te raken >> "))

def check_game():
    global game
    game = bool(input("toets 'enter' om de game te stoppen >> "))



def TikTakBoomTik(timeUntilBoom, timeUltilBoomMAX):
    # seconden omzetten naar milliseconden
    global game
    global value_touch

    timeBoom = float(time.time()) + timeUntilBoom
    timeLeft = timeUntilBoom
    lightActive = False
    knipperDelayTimeAbsoluut = 0
    firstTimeNearEnd = True
    touchWasActivated = False
    game = True

    # x = threading.Thread(target=check_touch, args=())
    # x.start()

    y = threading.Thread(target=check_game, args=())
    y.start()


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


        else:      # ------------TOUCH SENSOR IS GETIKT ---------------
            touchWasActivated = True
            break

        # check of de game nog bezig is  --------------->
        time.sleep(0.01)
        timeLeft = timeBoom - float(time.time())
    # ----------- END WHILE LOOP----------


    if touchWasActivated == False and game == True:
        # ----------------------------------------------
        # TIME IS OP --> kaboem
        # ------------------------------------------------
        print("KABAM")
        game = False

        # ontplof signaal duidelijk maken
        for x in range(0, 10):
            # show tik blauw met tone 200 -------------------->
            print("blauw")
            time.sleep(0.2)

            # show tik paars met tone 700  ----------------->
            print("paars")
            time.sleep(0.2)

        # show niets -------------->
        print("niets")

    elif touchWasActivated == True and game == True:
        # -----------------------------------------------
        # AFGETIKT
        # -------------------------------------------------

        # sent bericht naar de backend
        print("goed gedaan jonge")

        # aftik signaal
        # show tik appelblauw met tone 1000 -------------------->
        time.sleep(0.1)
        # show niets ------------>
        print("niets")

    elif game == False:
        # --------------------------------------------------
        # andere tik is ontploft of player stopt het spel
        # --------------------------------------------------
        # show tik paars met tone 700 -------------------->
        print("paars")
        time.sleep(0.2)
        # show niets -------------------->
        print("niets")
    

if __name__ == '__main__':
    TikTakBoomTik(timeUntilBoom, timeUltilBoomMAX)