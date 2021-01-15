const urlParams = new URLSearchParams(window.location.search);
const gameName = urlParams.get('gamename');

var playButton;

const loadPlayButtonHref = () => {
    playButton.setAttribute("href", `game.html?gamename=${gameName}`);
}

const getGameStartDomElements = () => {
    playButton = document.querySelector('.js-play-button');
}

const initGameStart = () => {
    console.log('Game start script loaded!');
    getGameStartDomElements();
    loadPlayButtonHref();
}

document.addEventListener('DOMContentLoaded', initGameStart);