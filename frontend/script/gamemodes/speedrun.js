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
        location.href = `game-end.html?gamename=${gameName}&score=${speedrunTimer.toFixed(2)}%20s&username=${userName}`
    });

    socket.on('B2F_speedrun_tiksleft', function (tiksLeft) {
        console.log(tiksLeft)
        tiksLeftHTML.innerHTML = tiksLeft;
    });
}

const listenToStop = () => {
    stopButton.addEventListener('click', function() {
        console.log("stoping")
        fetch(`http://${lanIP}/tiktem/v1/stopgame`)
        .catch((err) => console.error("An error occurd", err));

        countdownHTML.parentNode.style.display = "flex";
        countdownHTML.innerHTML = "STOP";


        setTimeout(function() {
            countdownHTML.parentNode.style.display = "none";
            window.location.href = `game-start.html?gamename=${gameName}`;
          }, 2000);
    })
}

const getSpeedrunDomElements = () => {
    speedrunTimerHTML = document.querySelector('.js-timer');
    tiksLeftHTML = document.querySelector('.js-speedrun-tiks-left');
    stopButton = document.querySelector('.js-stop-button');
}

const callBackStartGame = () => {
    console.log(`Starting ${gamemodeInfo[gameName].title}`);
    getSpeedrunDomElements();  
    runTimer(); 
    listenToSocket();
    listenToStop();
}