var menuContainer,tableContainer,selectButtons, leaderboardBack;  

const listenToButtons = () => {
    for(const select of selectButtons) {
        console.log(select)
        select.addEventListener('click', function() {
            menuContainer.classList.add('c-move-left');
            tableContainer.classList.add('c-move-left');
        })
    }

    leaderboardBack.addEventListener('click', function() {
        menuContainer.classList.remove('c-move-left');
        tableContainer.classList.remove('c-move-left');
    });

}

const getLeaderboardMenuDomElements = () => {
    menuContainer = document.querySelector('.js-leaderboard-menu-container');
    tableContainer = document.querySelector('.js-leaderboard-table-container');
    selectButtons = document.querySelectorAll('.js-leaderboard-select');
    leaderboardBack = document.querySelector('.js-leaderboard-back');
}

const initLeaderBoardMenu = () => {
    console.log('Countdown script loaded!')
    getLeaderboardMenuDomElements();
    listenToButtons();
}

document.addEventListener('DOMContentLoaded', initLeaderBoardMenu);