var colohuntScore, colorhuntTimer=30, colorhuntTimerHTML;

const runTimer = () => {
    y = setInterval(() => {
        colorhuntTimer -= 0.01;
        colorhuntTimerHTML.innerHTML = colorhuntTimer.toFixed(2);
    }, 10);
}


const listenToSocket = function () {
    socket.on('B2F_colorhunt_ended', function (score) {
        //console.log(score)
        location.href = `game-end.html?gamename=${gameName}&score=${score}%20punten&username=${userName}`
    });

    socket.on('B2F_colorhunt_score', function (score) {
        //console.log(score)
        colohuntScore.innerHTML = score;
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

const getColorhuntDomElements = () => {
    colohuntScore = document.querySelector('.js-score');
    stopButton = document.querySelector('.js-stop-button');
    colorhuntTimerHTML = document.querySelector('.js-timer');
}

const callBackStartGame = () => {
    console.log(`Starting ${gamemodeInfo[gameName].title}`);
    getColorhuntDomElements();  
    listenToSocket();
    listenToStop();
    runTimer();
}