const urlParams = new URLSearchParams(window.location.search);
const gameName = urlParams.get('gamename');

var mainContent, gameTitleHTML;

const loadGameScript = () => {
    var script = document.createElement('script');
    script.src = `script/gamemodes/${gameName}.js`;
    document.head.appendChild(script);
}

const loadGameHTML = () => {
    gameTitleHTML.innerHTML = gamemodeInfo[gameName].title
    mainContent.innerHTML += gamemodeInfo[gameName].html
}

const getGameDomElements = () => {
    gameTitleHTML = document.querySelector('.js-title');
    mainContent = document.querySelector('.js-main-content');
}

const initGame = () => {
    console.log('Game script loaded!');
    getGameDomElements();
    loadGameScript();
    loadGameHTML();
}

document.addEventListener('DOMContentLoaded', initGame);