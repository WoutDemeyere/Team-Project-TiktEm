var countdownHTML, number = 5, countdownEnd = false;

const handelCountdown = () => {
    x = setInterval(function() {
        console.log(number)
        number -= 1;

        if(number == 0) {
            countdownHTML.innerHTML = "GO";
        } else if(number < 0) { 
            startGame();
            countdownHTML.parentNode.style.display = "none";
            clearInterval(x);  
        } else {

            countdownHTML.innerHTML = number;      
            // countdownHTML.style.fontSize = "100px";
            // countdownHTML.style.fontSize = "50px";
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