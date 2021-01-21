var menuContainer,tableContainer,selectButtons, leaderboardBack, leaderboardTable, leaderboardTitle, selectedGame;  

const testdata = [
    {
        "name": "Jose vanseste",
        "gameid": "1",
        "scoretype": "s",
        "score": "24.46"
    },
    {
        "name": "Jose vanseste",
        "gameid": "1",
        "scoretype": "s",
        "score": "24.46"
    },
    {
        "name": "Jose vanseste",
        "gameid": "1",
        "scoretype": "s",
        "score": "24.46"
    },
    {
        "name": "Jose vanseste",
        "gameid": "1",
        "scoretype": "s",
        "score": "24.46"
    },
    {
        "name": "Jose vanseste",
        "gameid": "1",
        "scoretype": "s",
        "score": "24.46"
    },
    {
        "name": "Jose vanseste",
        "gameid": "1",
        "scoretype": "s",
        "score": "24.46"
    },
    {
        "name": "Jose vanseste",
        "gameid": "1",
        "scoretype": "s",
        "score": "24.46"
    },
    {
        "name": "Jose vanseste",
        "gameid": "1",
        "scoretype": "s",
        "score": "24.46"
    },
    {
        "name": "Jose vanseste",
        "gameid": "1",
        "scoretype": "s",
        "score": "24.46"
    }
]

// const loadLeaderboard = () => {
//     htmlString = `  <tr class="c-table-header">
//                         <th class="c-table-header__text">Plaats</th>
//                         <th class="c-table-header__text">Naam</th>
//                         <th class="c-table-header__text">Score</th>
//                     </tr>`;

//     for(var i = 0; i < testdata.length; i++) {
//         if(i < 3) {
//             htmlString += ` <tr class="c-table-row c-talbe-row-${i+1}">
//                                 <td class="c-table-row-text">${i+1}</td>
//                                 <td class="c-table-row-text">${testdata[i].name}</td>
//                                 <td class="c-table-row-text">${testdata[i].score}</td>
//                             </tr>`
//         } else {
//             htmlString += ` <tr class="c-table-row">
//                                 <td class="c-table-row-text">${i+1}</td>
//                                 <td class="c-table-row-text">${testdata[i].name}</td>
//                                 <td class="c-table-row-text">${testdata[i].score}</td>
//                             </tr>`
//         }
//     }

//     leaderboardTable.innerHTML = htmlString;
// }

const loadTable = (name) => {
    leaderboardTitle.innerHTML = gamemodeInfo[name].title;

    leaderBoardFilterOpen.addEventListener('click', function() {
        leaderBoardFilterOpen.parentNode.classList.toggle('c-leaderboard__filter-colapse')
    })

    leaderboard = new Leaderboard(leaderboardTable, name)
    leaderboard.loadLeaderboardData();

    
}

const listenToButtons = () => {
    for(const select of selectButtons) {
        select.addEventListener('click', function() {
            menuContainer.classList.add('c-move-left');
            tableContainer.classList.add('c-move-left');

            selectedGame = select.getAttribute('gamename')
            loadTable(selectedGame);
        })
    }

    leaderboardBack.addEventListener('click', function() {
        menuContainer.classList.remove('c-move-left');
        tableContainer.classList.remove('c-move-left');
    });

    leaderBoardFilter.addEventListener('input', function() {
        leaderboard.filterLeaderboard(leaderBoardFilter.value)
    })
}

const getLeaderboardMenuDomElements = () => {
    menuContainer = document.querySelector('.js-leaderboard-menu-container');
    tableContainer = document.querySelector('.js-leaderboard-table-container');
    selectButtons = document.querySelectorAll('.js-leaderboard-select');
    leaderboardBack = document.querySelector('.js-leaderboard-back');
    leaderboardTable = document.querySelector('.js-leaderboard-table');
    leaderboardTitle = document.querySelector('.js-leaderboard-title');
    leaderBoardFilter = document.querySelector('.js-leaderboard-filter');
    leaderBoardFilterOpen = document.querySelector('.js-open-filter');
}

const initLeaderBoardMenu = () => {
    console.log('Countdown script loaded!')
    getLeaderboardMenuDomElements();
    listenToButtons();
}

document.addEventListener('DOMContentLoaded', initLeaderBoardMenu);