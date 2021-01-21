const urlParams = new URLSearchParams(window.location.search);
const gameName = urlParams.get('gamename');

var playButton, tableContainer;

const listenToPlayButton = () => {
    playButton.addEventListener('click', function() {
        username = usernameInput.value;

        if(!isEmpty(username)) {
            location.href = `game.html?gamename=${gameName}&username=${username}`
            usernameInput.classList.remove('c-input-error');
            document.querySelector('.js-error-text').style.transform = "translate(0, 40px)"
        } else {
            usernameInput.classList.add('c-input-error');
            document.querySelector('.js-error-text').style.transform = "translate(0, 0)"
        }  

    })
}

const loadGameThings = () => {
    playButton.setAttribute("href", `game.html?gamename=${gameName}`);
    leaderboard = new Leaderboard(tableContainer, gameName, 5);
    leaderboard.loadLeaderboardData();
}

const getGameStartDomElements = () => {
    tableContainer = document.querySelector('.js-leaderboard-table');
    playButton = document.querySelector('.js-play-button');
    usernameInput = document.querySelector('.js-email-input');
}

const initGameStart = () => {
    console.log('Game start script loaded!');
    getGameStartDomElements();
    loadGameThings();
    listenToPlayButton();
}

document.addEventListener('DOMContentLoaded', initGameStart);