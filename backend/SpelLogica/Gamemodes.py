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
    time.sleep(8)
    print(f"Congratulations you finished colorhunt with a score of {colorhuntscore} ")
    socketio.emit("B2F_score", colorhuntscore,broadcast=True)