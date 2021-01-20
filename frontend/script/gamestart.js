const urlParams = new URLSearchParams(window.location.search);
const gameName = urlParams.get('gamename');

var playButton, tableContainer;

const listenToPlayButton = () => {
    playButton.addEventListener('click', function() {
        location.href = "game.html?gamename=${gameName}"
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
}

const initGameStart = () => {
    console.log('Game start script loaded!');
    getGameStartDomElements();
    loadGameThings();
    listenToPlayButton();
}

document.addEventListener('DOMContentLoaded', initGameStart);