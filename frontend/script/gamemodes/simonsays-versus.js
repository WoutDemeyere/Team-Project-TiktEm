const listenToSocket = function () {
    socket.on('B2F_simonsaysvs_ended', function (score) {
        console.log(score)
        location.href = `game-end.html?gamename=${gameName}&score=${score}%20punten&username=${userName}`
    });

    socket.on('B2F_simonsaysvs_score_1', function (score) {
        console.log(score)
        score1.innerHTML = score;
    });

    socket.on('B2F_simonsaysvs_score_2', function (score) {
        console.log(score)
        score2.innerHTML = score;
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

const getSimonSaysVSDomElements = () => {
    score1 = document.querySelector('.js-score-1');
    score2 = document.querySelector('.js-score-2');
    stopButton = document.querySelector('.js-stop-button');
}

const callBackStartGame = () => {
    console.log(`Starting ${gamemodeInfo[gameName].title}`);
    getSimonSaysVSDomElements();  
    listenToSocket();
    listenToStop();
}