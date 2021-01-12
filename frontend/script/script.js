var mainContent, singleplayerButton, multiplayerButton, singleplayerContainer, multiplayerContainer;

const listenToCollapsables = () => {
    singleplayerButton.addEventListener('click', function() {
        foldMulti()
        collapseSingle();
        
    })

    multiplayerButton.addEventListener('click', function() {
        foldSingle();
        collapseMulti();
       
    })
}

const collapseSingle  = function() {
    mainContent.classList.add('c-collapsed');
    singleplayerContainer.classList.add("c-icon-button-container--collapsed");
    singleplayerButton.style.display = "none";
    document.querySelector('.js-single-hidden-options').style.height = "100%";
}

const foldSingle = function() {
    singleplayerContainer.classList.remove("c-icon-button-container--collapsed");
    singleplayerButton.style.display = "block";
    document.querySelector('.js-single-hidden-options').style.height = "0";
}
 
const collapseMulti = function() {
    mainContent.classList.add('c-collapsed');
    multiplayerContainer.classList.add("c-icon-button-container--collapsed");
    multiplayerButton.style.display = "none";
    document.querySelector('.js-multi-hidden-options').style.height = "100%";
}

const foldMulti = function() {
    multiplayerContainer.classList.remove("c-icon-button-container--collapsed");
    multiplayerButton.style.display = "block";
    document.querySelector('.js-multi-hidden-options').style.height = "0";
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