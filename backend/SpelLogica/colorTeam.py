from Models.Tik import Tik
from Models.TiktEm import TiktEm
import threading
import random

tiktem=TiktEm("client",4)
tiktem.init_tiks()
global1=0
global2=0
winner=""
def colorteam():
    #TiktEm.reset_tiks()
    #2 teams
    team=[{"color":"blue","sequence":0,"team":1},{"color":"red","sequence":0,"team":2}]
    #firtst button of sequence of both teams
    x = threading.Thread(target=colorteamCheck, args=(team[0]))
    x.start()
    y = threading.Thread(target=colorteamCheck, args=(team[1]))
    y.start()
    print(team)
    while(True):
        if(global1):
            team[0]["sequence"]+=1
            print(f"team2 have pushed the {team[0]['sequence']}e button")
            global1=0
            x = threading.Thread(target=colorteamCheck, args=(team[0]))
            x.start()
        if(global2):
            team[1]["sequence"]+=1
            print(f"team2 have pushed the {team[1]['sequence']}e button")
            global2=0
            y = threading.Thread(target=colorteamCheck, args=(team[1]))
            y.start()
        #kan ook in for loop
        if(team[0]["sequence"]==10):
            print(f"team {team[0]['color']} has won")
            winner=team[0]['color']
            break
        elif(team[1]["sequence"]==10):
            print(f"team {team[1]['color']} has won")
            winner=team[1]['color']
            break
def colorteamCheck(team):
    openTiks=[]
    #checking wich tik available
    for tik in tiktem.tiks:
        lightstatus=tiktem.get_colorhunt_status(tik.id)
        if(lightstatus==False):
            openTiks.append(tik)
        #select possible tik
        selection=random.randint(0,len(openTiks)-1)
        #light up selected light
        active=True
        r=0
        g=0
        b=0
        if(team["color"]=="red"):
            r=255
        elif(team["color"=="green"]):
            g=255
        elif(team["color"=="blue"]):
            b=255
        tiktem.tiks[selection].turn_on(r, g, b, 500)
        #check if selected light gets pushed
        while active == True:
            #checking push status of selected tik
            value = tiktem.get_tik_status(tiktem.tiks[selection])
            value=input("give input for",team["team"])
            if value == True:
                active = False
                tiktem.tiks[selection].turn_off()
                #checking what team this tik belongs to
                if(team["team"]==1):
                    global1=1
                elif(team["team"]==2):
                    global2=1
     
    

colorteam()