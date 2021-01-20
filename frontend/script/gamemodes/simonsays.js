var simonScore, stopButton, score;


const listenToSocket = function () {
    socket.on('B2F_simonsays_ended', function (score) {
        console.log(score)
        location.href = `game-end.html?gamename=${gameName}&score=${score}&username=${userName}`
    });

    socket.on('B2F_simonsays_sequence', function (sequence) {
        console.log(sequence)
        simonScore.innerHTML = sequence;
    });
}

const listenToStop = () => {
    stopButton.addEventListener('click', function() {
        fetch(`http://${lanIP}/tiktem/v1/stopgame`)
        .catch((err) => console.error("An error occurd", err));
    })
}

const getSimonSaysDomElements = () => {
    simonScore = document.querySelector('.js-score');
    stopButton = document.querySelector('.js-stop');
}

const callBackStartGame = () => {
    console.log(`Starting ${gamemodeInfo[gameName].title}`);
    getSimonSaysDomElements();  
    listenToSocket();
}