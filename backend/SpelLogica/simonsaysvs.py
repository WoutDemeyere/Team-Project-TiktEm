def simonSays():
    playeramount = 2
    tiktem.reset_tiks()
    tiktem.game_on = True
    tiktem.score = 0
    player = 1
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

                                    if tik.id == i:         # JUIST
                                        tik.turn_on_delay(0, 255, 0, 800, 300)
                                        time.sleep(0.6)

                                    elif tik.id != i:       # FOUT
                                        tik.turn_on_delay(255, 0, 0, 200, 500)
                                        tiktem.game_on = False
                                        print(f"\n+++++ Wrong Tik player {player} lost +++++\n")
                                        socketio.emit("B2F_score", tiktem.score, broadcast=True)
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
                            tik.turn_on(0,0,255, 800)
                            time.sleep(0.4)
                            tik.turn_off()
                            time.sleep(1)
                            sequence.append[tik.id]
                            waiting = False
            
            if player == playeramount:
                player = 1
            else:
                player +=1



