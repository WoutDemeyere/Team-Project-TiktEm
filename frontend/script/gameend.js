const urlParams = new URLSearchParams(window.location.search);
const gameName = urlParams.get('gamename');
const score = urlParams.get('score');
const userName = urlParams.get('username');

var resultContainer, tableContainer, playButton;

const loadResultHTML = () => {
    resultContainer.innerHTML = gamemodeInfo[gameName].htmlResult;
   
    if(gamemodeInfo[gameName].id>4) {
        console.log(score)
        document.querySelector('.js-score').innerHTML = score;
        document.querySelector('.c-leaderboard-sm-container').style.display = 'none'; 
    } else {
        document.querySelector('.js-score').innerHTML = score;
        leaderboard = new Leaderboard(tableContainer, gameName, 5);
        leaderboard.loadLeaderboardData(userName);
    }

    
}

const listenToPlayButton = () => {
    playButton.addEventListener('click', function() {
        location.href = `game-start.html?gamename=${gameName}`
    })
}

const getGameEndDomElements = () => {
    resultContainer = document.querySelector('.js-result-container');
    tableContainer = document.querySelector('.js-leaderboard-table');
    playButton = document.querySelector('.js-play-button');

}

const initGameEnd = () => {
    console.log('Game end script loaded!');
    getGameEndDomElements();
    listenToPlayButton();
    loadResultHTML();
}

document.addEventListener('DOMContentLoaded', initGameEnd);