var speedrunTimerHTML, tiksLeftHTML,  speedrunTimer = 0, tiksLeft;

const runTimer = () => {
    y = setInterval(() => {
        speedrunTimer += 0.01;
        speedrunTimerHTML.innerHTML = speedrunTimer.toFixed(2);
    }, 10);
}

const startGame = () => {
    runTimer();
}

const getSpeedrunDomElements = () => {
    speedrunTimerHTML = document.querySelector('.js-timer');
    tiksLeftHTML = document.querySelector('.js-speedrun-tiks-left');
}

const initSpeedrun = () => {
    console.log('Speedrun script loaded!')
    getSpeedrunDomElements();
}

document.addEventListener('DOMContentLoaded', initSpeedrun);