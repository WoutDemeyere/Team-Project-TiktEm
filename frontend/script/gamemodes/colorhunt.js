var colohuntScore


const listenToSocket = function () {
    socket.on('B2F_colorhunt_ended', function (score) {
        console.log(score)
        location.href = `game-end.html?gamename=${gameName}&score=${score}%20punten&username=${userName}`
    });

    socket.on('B2F_colorhunt_score', function (score) {
        console.log(score)
        colohuntScore.innerHTML = score;
    });
}

const listenToStop = () => {
    stopButton.addEventListener('click', function() {
        fetch(`http://${lanIP}/tiktem/v1/stopgame`)
        .catch((err) => console.error("An error occurd", err));
    })
}

const getColorhuntDomElements = () => {
    colohuntScore = document.querySelector('.js-score');
    stopButton = document.querySelector('.js-stop');
}

const callBackStartGame = () => {
    console.log(`Starting ${gamemodeInfo[gameName].title}`);
    getColorhuntDomElements();  
    listenToSocket();
}