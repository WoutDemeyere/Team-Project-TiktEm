const urlParams = new URLSearchParams(window.location.search);
const gameName = urlParams.get('gamename');

var playButton, tableContainer;

const listenToPlayButton = () => {
    playButton.addEventListener('click', function() {
        username = usernameInput.value;

        if(!isEmpty(username)) {
            Cookies.set('username', username)
            location.href = `game.html?gamename=${gameName}&username=${username}`
            usernameInput.classList.remove('c-input-error');
            document.querySelector('.js-error-text').style.transform = "translate(0, 40px)"
        } else {
            usernameInput.classList.add('c-input-error');
            document.querySelector('.js-error-text').style.transform = "translate(0, 0)"
        }  

    })
}

const loadGameThings = () => {
    playButton.setAttribute("href", `game.html?gamename=${gameName}`);

    if(gamemodeInfo[gameName].id>4) {
        tableContainer.innerHTML = `<tr class="c-table-row c-table-row--message-container"> 
                                        <td class="c-table-row--message">This gamemode has no leaderboard</td>      
                                    </tr>`  
    } else {
        leaderboard = new Leaderboard(tableContainer, gameName, 5);
        leaderboard.loadLeaderboardData();
    }
    
}

const getGameStartDomElements = () => {
    tableContainer = document.querySelector('.js-leaderboard-table');
    playButton = document.querySelector('.js-play-button');
    usernameInput = document.querySelector('.js-email-input');

    console.log(Cookies.get('username'))
    if(Cookies.get('username') != undefined)usernameInput.value = Cookies.get('username')
}

const initGameStart = () => {
    console.log('Game start script loaded!');
    getGameStartDomElements();
    loadGameThings();
    listenToPlayButton();
}

document.addEventListener('DOMContentLoaded', initGameStart);