var speedrunTimerHTML, tiksLeftHTML,  speedrunTimer = 0, tiksLeft;

const runTimer = () => {
    y = setInterval(() => {
        speedrunTimer += 0.01;
        speedrunTimerHTML.innerHTML = speedrunTimer.toFixed(2);

        if(speedrunTimer >= 5) {
            location.href = `game-end.html`
        }
    }, 10);
}

const getSpeedrunDomElements = () => {
    speedrunTimerHTML = document.querySelector('.js-timer');
    tiksLeftHTML = document.querySelector('.js-speedrun-tiks-left');
}

const callBackStartGame = () => {
    console.log(`Starting ${gamemodeInfo[gamename].title}`);
    getSpeedrunDomElements();  
    runTimer(); 
}