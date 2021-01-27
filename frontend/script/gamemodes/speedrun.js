var speedrunTimerHTML, tiksLeftHTML,  speedrunTimer = 0, tiksLeft, stopButton;

const runTimer = () => {
    y = setInterval(() => {
        speedrunTimer += 0.01;
        speedrunTimerHTML.innerHTML = speedrunTimer.toFixed(2);
    }, 10);
}

const listenToSocket = function () {
    console.log("U DIKKE MAMA")

    socket.emit('yeet', 'yeeteerskeeter');
    
    socket.on('B2F_speedrun_ended', function (score) {
        //console.log("ENDEN")
        //console.log(score)

        clearInterval(y);
        stopGame();
        
        location.href = `game-end.html?gamename=${gameName}&score=${speedrunTimer.toFixed(2)}%20s&username=${userName}`
    });

    socket.on('B2F_speedrun_tiksleft', function (tiksLeft) {
        //console.log("TIKS LEFT")
        //console.log(tiksLeft)
        tiksLeftHTML.innerHTML = tiksLeft;
    });
}

const listenToStop = () => {
    stopButton.addEventListener('click', function() {
        console.log("stoping")
        stopGame();

        countdownHTML.parentNode.style.display = "flex";
        countdownHTML.innerHTML = "STOP";


        setTimeout(function() {
            countdownHTML.parentNode.style.display = "none";
            window.location.href = `game-start.html?gamename=${gameName}`;
          }, 2000);
    })
}

const stopGame = () => {
    fetch(`http://${lanIP}/tiktem/v1/stopgame`)
    .catch((err) => console.error("An error occurd", err));
}

const getSpeedrunDomElements = () => {
    speedrunTimerHTML = document.querySelector('.js-timer');
    tiksLeftHTML = document.querySelector('.js-speedrun-tiks-left');
    stopButton = document.querySelector('.js-stop-button');
}

const callBackStartGame = () => {
    console.log(`Starting ${gamemodeInfo[gameName].title}`);
    getSpeedrunDomElements();  
    listenToSocket();
    runTimer(); 
    listenToStop();

    console.log(socket)
}