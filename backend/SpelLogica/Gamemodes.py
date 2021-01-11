def colorhuntlight(colorhunttype,tikid):
    time.sleep(2)
    if(colorhunttype == 0):
        tiktem.tiks[tikid].turn_on(255, 0, 0, 800)
        starttime = datetime.now()
        currenttime = datetime.now()
            while((currenttime - starttime).total_seconds() < 3):
                value = tiktem.get_tik_status(tikid)
                if(value==1):
                    tiktem.tiks[tikid].turn_off()
                    colorhuntscore += 10
                    return ""
        #3 seconds rood
    elif(colorhunttype == 1):
        tiktem.tiks[tikid].turn_on(0, 0, 255, 800)
        starttime = datetime.now()
        currenttime = datetime.now()
            while((currenttime - starttime).total_seconds() < 5):
                value = tiktem.get_tik_status(tikid)
                if(value==1):
                    tiktem.tiks[tikid].turn_off()
                    colorhuntscore += 4
                    return ""
        #5 seconds blauw
    elif(colorhunttype == 2):
        tiktem.tiks[tikid].turn_on(0, 255, 0, 800)
        starttime = datetime.now()
        currenttime = datetime.now()
            while((currenttime - starttime).total_seconds() < 8):
                value = tiktem.get_tik_status(tikid)
                if(value==1):
                    tiktem.tiks[tikid].turn_off()
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
    while((currenttime - starttime).total_seconds() < 60):
        for item in tiks:
            value = tiktem.get_tik_status(item.id)
            if(value==1):
                colortype = random.randint(0,2)
                x = threading.Thread(target=colorhuntlight, args=(colortype,item.id))
                x.start()
    time.sleep(8)
    print(f"Congratulations you finished colorhunt with a score of {colorhuntscore} ")
    socketio.emit("B2F_score", colorhuntscore,broadcast=True)


def simonsaysvs():
    playeramount = 2
    tiktem.reset_tiks()
    game = True
    sequence = []
    sequence.append(random.randint(0,1))
    player = 1
    players = []
    for i in range(1,playeramount+1):
        players.append(True)

    while(game == True):
        # sequence.append(random.randint(0,1))
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
                            print(f"Wrong Tik you are eliminated")
                            players[player] = False
                            break    
        
        if players[player] == True
            waiting = True
            while waiting:
                for tik in tiktem.tiks:
                    if tiktem.get_tik_status(tik.id) == True:
                        tik.turn_on(0,0,255, 800)
                        time.sleep(0.4)
                        tik.turn_off()
                        time.sleep(1)
                        sequence.append[tik.id]
                        waiting = False
        counter = 0
        for i in players:
            if i == False:
                counter + 1
        if counter == playeramount - 1:
            for i in range(1,playeramount+1):
                if players[i] == True:
                    print(f"Player {i} won!")
                    socketio.emit("B2F_score", player,broadcast=True)

        if player == playeramount:
            player = 1
        else:
            player +=1