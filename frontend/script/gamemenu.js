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

const getDomElements = () => {
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