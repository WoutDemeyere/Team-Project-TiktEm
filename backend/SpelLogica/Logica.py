from Models.Tik import Tik
import time
from datetime import datetime

def menu():
    tiks = initTiks()
    print(f"Kies een optie in het menu")
    print(f"0: Begin spel")
    print(f"1: List tiks")
    print(f"2: close")
    value = input("Uw keuze: ")
    if(value == "0"):
        initGame(tiks)
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


def initGame(tiks):
    print(f"Game starting")
    time.sleep(1)
    print(f"3..")
    time.sleep(1)
    print(f"2..")
    time.sleep(1)
    print(f"1..")
    time.sleep(1)
    print(f"Start")
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





def turnOn(item):
    item.tikstatus = True
    item.lightstatus = True
    item.green = 256
    item.red = 0
    item.blue = 0
    # Send to correct tik via mqtt


menu()