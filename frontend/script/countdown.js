var countdownHTML, number = 5, countdownEnd = false;

const handelCountdown = () => {
    x = setInterval(function() {
        console.log(number)
        number -= 1;

        if(number == 0) {
            countdownHTML.innerHTML = "GO";
        } else if(number < 0) { 
            clearInterval(x);  
            handleData(`http://${lanIP}/tiktem/v1/startgame?gameid=${gamemodeInfo[gamename].id}`, callBackStartGame, callbackShowErrorGame, "GET", null);
            countdownHTML.parentNode.style.display = "none";
        } else {
            countdownHTML.innerHTML = number;      
        }

    }, 1000)
}

const getCountdownDomElements = () => {
    countdownHTML = document.querySelector('.js-countdown');
}

const initCountdown = () => {
    console.log('Countdown script loaded!')
    getCountdownDomElements();
    handelCountdown();
}

document.addEventListener('DOMContentLoaded', initCountdown);