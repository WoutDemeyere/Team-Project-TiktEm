var tiktakScore;

const listenToSocket = function () {
    socket.on('B2F_tiktak_ended', function (score) {
        console.log(score)
        location.href = `game-end.html?gamename=${gameName}&score=${score}%20punten&username=${userName}`
    });

    socket.on('B2F_tiktak_score', function (score) {
        console.log(score)
        tiktakScore.innerHTML = score;
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

const getTikTakBoemDomElements = () => {
    tiktakScore = document.querySelector('.js-score');
    stopButton = document.querySelector('.js-stop-button');
}

const callBackStartGame = () => {
    console.log(`Starting ${gamemodeInfo[gameName].title}`);
    getTikTakBoemDomElements();  
    listenToSocket();
    listenToStop();
}