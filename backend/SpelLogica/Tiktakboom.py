import random
import threading
import time
from Models.TiktEm import TiktEm

timeUltilBoomMIN = 15
timeUltilBoomMAX = 35
game = True
score = 0


def TikTakBoom():
    global game
    global score
    score = 0
    game = True
    for tik in range(0, 4):
        TikTakBoomThread(tik)


def TikTakBoomThread(tik):
    global game
    global score

    timeUntilBoom = random.randint(timeUltilBoomMIN, timeUltilBoomMAX)
    # sent de tik.id de timeUntilBoom & timeUltilBoomMAX

    while game == True:
        # get tik touch value
        valueTouch = TiktEm.get_tik_status(item.id)
        if valueTouch == True:
            score += 1
            time.sleep(4)
            if game == True:
                timeUntilBoom = random.randint(
                    timeUltilBoomMIN, timeUltilBoomMAX)
                # sent tik.id de timeUntilBoom & timeUltilBoomMAX

        # get tik ontploft value
        valueBoom = TiktEm.get_tik_status_ontploft(item.id)
        if valueBoom == True:
            game = False

    # GAME ENDED
    # sent tik.id dat het spel gedaan is


if __name__ == '__main__':
    TikTakBoom()
