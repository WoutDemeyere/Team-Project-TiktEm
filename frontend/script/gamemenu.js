var mainContent, singleplayerButton, multiplayerButton, singleplayerContainer, multiplayerContainer;


const listenToCollapsables = () => {
    singleplayerButton.addEventListener('click', function() {
        multiplayerButton.parentNode.parentNode.classList.remove('c-has-collapsed')
        this.parentNode.parentNode.classList.add('c-has-collapsed')
        mainContent.classList.add('c-collapsed')
    })  

    multiplayerButton.addEventListener('click', function() {
        singleplayerButton.parentNode.parentNode.classList.remove('c-has-collapsed');
        this.parentNode.parentNode.classList.add('c-has-collapsed'); 
        mainContent.classList.add('c-collapsed')
    })  
}

const loadInGameInfo = async () => {
    await reloadGameInfo();

    for(var option of gameOptions) {
        currId = option.getAttribute('gameid');

        for(var info in gamemodeInfo) {
            if(currId==gamemodeInfo[info].id) {
                option.querySelector('.js-title').innerHTML = gamemodeInfo[info].title
                option.querySelector('.js-desc').innerHTML = gamemodeInfo[info].desc
            }
        }
    }
}

const resetTiks = () => {
    fetch(`http://${lanIP}/tiktem/v1/reset`, {
        method: "GET"})
    .catch((err) => console.error("An error occurd", err));
}

const getDomElements = () => {
    mainContent = document.querySelector('.js-main-content');
    singleplayerButton = document.querySelector('.js-single');
    multiplayerButton = document.querySelector('.js-multi');
    gameOptions = document.querySelectorAll('.js-game-option')
}

const init = () => {
    console.log('Script loaded!')
    getDomElements();
    loadInGameInfo();
    resetTiks();
    listenToCollapsables();
}


document.addEventListener('DOMContentLoaded', init);