const urlParams = new URLSearchParams(window.location.search);
const gameName = urlParams.get('gamename');
const score = urlParams.get('score');

var resultContainer, tableContainer;

const loadResultHTML = () => {
    resultContainer.innerHTML = gamemodeInfo[gameName].htmlResult;
    document.querySelector('.js-score').innerHTML = score;
    loadLeaderboard(tableContainer, gameName, 5)
}

const getGameEndDomElements = () => {
    resultContainer = document.querySelector('.js-result-container');
    tableContainer = document.querySelector('.js-leaderboard-table');
}

const initGameEnd = () => {
    console.log('Game end script loaded!');
    getGameEndDomElements();
    loadResultHTML();
}

document.addEventListener('DOMContentLoaded', initGameEnd);