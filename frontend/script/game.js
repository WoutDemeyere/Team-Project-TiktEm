const urlParams = new URLSearchParams(window.location.search);
const gameName = urlParams.get('gamename');

const socket = io(`http://${lanIP}`);

var mainContent, gameTitleHTML;
var countdownHTML, number = 1, countdownEnd = false;

const handelCountdown = () => {
    x = setInterval(function() {
        console.log(number)
        number -= 1;

        if(number == 0) {
            countdownHTML.innerHTML = "GO";
        } else if(number < 0) { 
            clearInterval(x);  

            fetch(`http://${lanIP}/tiktem/v1/startgame?gameid=${gamemodeInfo[gameName].id}`)
            .catch((err) => console.error("An error occurd", err));
            callBackStartGame();

            countdownHTML.parentNode.style.display = "none";
        } else {
            countdownHTML.innerHTML = number;      
        }

    }, 1000)
}

const loadGameScript = () => {
    var script = document.createElement('script');
    script.src = `script/gamemodes/${gameName}.js`;
    document.head.appendChild(script);
}

const loadGameHTML = () => {
    gameTitleHTML.innerHTML = gamemodeInfo[gameName].title
    mainContent.innerHTML += gamemodeInfo[gameName].html
}

const callbackShowErrorGame = () => {
    console.error(`Error at ${gamemodeInfo[gameName].title} start`)
    alert('Er ging iets mis in de backend')
}

const getGameDomElements = () => {
    countdownHTML = document.querySelector('.js-countdown');
    gameTitleHTML = document.querySelector('.js-title');
    mainContent = document.querySelector('.js-main-content');
}
    
const initGame = () => {
    console.log('Game script loaded!');
    getGameDomElements();
    handelCountdown();
    loadGameScript();
    loadGameHTML();

}

document.addEventListener('DOMContentLoaded', initGame);