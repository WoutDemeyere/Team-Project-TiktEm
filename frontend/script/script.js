var mainContent, singleplayerButton, multiplayerButton, singleplayerContainer, multiplayerContainer;

const listenToCollapsables = () => {
    singleplayerButton.addEventListener('click', function() {
        mainContent.classList.add('c-collapsed');

        singleplayerContainer.innerHTML = "";
        singleplayerContainer.classList.add("c-icon-button-container--collapsed");

        singleplayerContainer.innerHTML = "";
    })
}

const getDomElements = function() {
    mainContent = document.querySelector('.js-main-content');
    singleplayerButton = document.querySelector('.js-single');
    multiplayerButton = document.querySelector('.js-multi');

    singleplayerContainer = document.querySelector('.js-single-container');
    multiplayerContainer = document.querySelector('.js-multi-container');
}

const init = () => {
    console.log('Script loaded!')
    getDomElements();

    listenToCollapsables();
}


document.addEventListener('DOMContentLoaded', init);