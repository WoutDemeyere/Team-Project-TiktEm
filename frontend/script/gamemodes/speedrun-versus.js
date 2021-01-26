const listenToSocket = function () {
    socket.on('B2F_colorteam_ended', function (score) {
        //console.log('ENDED')
        //console.log(score)
        location.href = `game-end.html?gamename=${gameName}&score=${score}`
    });

    socket.on('B2F_colorteam_score_red', function (score) {
        //console.log(score)
        scoreRed.innerHTML = score;
    });

    socket.on('B2F_colorteam_score_blue', function (score) {
        //console.log(score)
        scoreBlue.innerHTML = score;
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

const getColorTeamDomElements = () => {
    scoreRed = document.querySelector('.js-score-red');
    scoreBlue = document.querySelector('.js-score-blue');
    stopButton = document.querySelector('.js-stop-button');
}

const callBackStartGame = () => {
    console.log(`Starting ${gamemodeInfo[gameName].title}`);
    getColorTeamDomElements();  
    listenToSocket();
    listenToStop();
}