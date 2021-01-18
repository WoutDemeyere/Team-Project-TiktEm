var speedrunTimerHTML, tiksLeftHTML,  speedrunTimer = 0, tiksLeft, stopButton;

const runTimer = () => {
    y = setInterval(() => {
        speedrunTimer += 0.01;
        speedrunTimerHTML.innerHTML = speedrunTimer.toFixed(2);
    }, 10);
}

const listenToSocket = function () {
    socket.on('B2F_speedrun_ended', function (score) {
        console.log(score)

        clearInterval(y);
        location.href = `game-end.html?gamename=${gameName}&score=${speedrunTimer.toFixed(2)}%20s`
    });

    socket.on('B2F_speedrun_tiksleft', function (tiksLeft) {
        console.log(tiksLeft)
        tiksLeftHTML.innerHTML = tiksLeft;
    });
}

const listenToStop = () => {
    stopButton.addEventListener('click', function() {
        fetch(`http://${lanIP}/tiktem/v1/stopgame`)
        .catch((err) => console.error("An error occurd", err));
    })
}

const getSpeedrunDomElements = () => {
    speedrunTimerHTML = document.querySelector('.js-timer');
    tiksLeftHTML = document.querySelector('.js-speedrun-tiks-left');
    stopButton = document.querySelector('.js-stop');
}

const callBackStartGame = () => {
    console.log(`Starting ${gamemodeInfo[gameName].title}`);
    getSpeedrunDomElements();  
    runTimer(); 
    listenToSocket();
}