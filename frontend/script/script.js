var mainContent, singleplayerButton, multiplayerButton, singleplayerContainer, multiplayerContainer;

const listenToCollapsables = () => {
    singleplayerButton.addEventListener('click', function() {
        this.parentNode.style.flexGrow = "1";
        multiplayerButton.parentNode.style.flexGrow = "0";
        mainContent.classList.add('c-collapsed')
    })  

    multiplayerButton.addEventListener('click', function() {
        this.parentNode.style.flexGrow = "1";
        singleplayerButton.parentNode.style.flexGrow = "0";
        mainContent.classList.add('c-collapsed')
    })  
}

const getDomElements = function() {
    mainContent = document.querySelector('.js-main-content');
    singleplayerButton = document.querySelector('.js-single');
    multiplayerButton = document.querySelector('.js-multi');
}

const init = () => {
    console.log('Script loaded!')
    getDomElements();
    listenToCollapsables();
}


document.addEventListener('DOMContentLoaded', init);