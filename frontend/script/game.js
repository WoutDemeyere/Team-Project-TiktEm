const urlParams = new URLSearchParams(window.location.search);
const gameName = urlParams.get('gamename');
const userName = urlParams.get('username');

// const socket = io(`http://${lanIP}`);
const socket = io(`http://${window.location.hostname}:5000`);
console.log(socket)

var mainContent, gameTitleHTML;
var countdownHTML, number = 5, countdownEnd = false;

const handelCountdown = () => {
    x = setInterval(function() {
        console.log(number)
        number -= 1;

        if(number == 0) {
            countdownHTML.innerHTML = "GO";
        } else if(number < 0) { 
            clearInterval(x);  

            fetch(`http://${lanIP}/tiktem/v1/startgame?gameid=${gamemodeInfo[gameName].id}&username=${userName}`)
            .then( response => {
                stat = response.json()
                if (!response.ok) {
                    window.alert("Er is al een game bezig") 
                    window.location.href = `gamemenu.html`
                } 
                //return stat.  //we only get here if there is no error
              })
            .catch((err) => console.error("An error occurd", err));
            callBackStartGame();

            countdownHTML.parentNode.style.display = "none";
        } else {
            countdownHTML.innerHTML = number;      
        }

    }, 1000)
}

const stoppGame = () => {
    fetch(`http://${lanIP}/tiktem/v1/stopgame`)
    .catch((err) => console.error("An error occurd", err));
}

const loadGameScript = () => {
    var script = document.createElement('script');
    script.src = `script/gamemodes/${gameName}.js`;
    document.head.appendChild(script);
}

const loadGameHTML = () => {   
    gameTitleHTML.innerHTML = gamemodeInfo[gameName].title
    mainContent.innerHTML += gamemodeInfo[gameName].html

    console.log(gamemodeInfo[gameName])
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

    socket.on("connect", function () {
        console.log("Verbonden met de socekt")
    });

}

document.addEventListener('DOMContentLoaded', initGame);