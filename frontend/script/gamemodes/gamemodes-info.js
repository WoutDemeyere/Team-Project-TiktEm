const gamemodeInfo = {
    "speedrun": {
        "title": "Speedrun",
        "id": 1,
        "html": `<div class="c-game-info-container">
                    <p class="c-game-info__header">Verstreken tijd</p>
                    <p class="c-game-time__time js-timer">00.00</p>
                </div>

                <div class="c-game-info-container">
                    <p class="c-game-info__header">Te tikken Tiks</p>
                    <p class="c-game-info__tiks js-speedrun-tiks-left">0</p>
                </div>
                
                <div class="c-play-button-container">
                        <a href="game.html?gamename=speedrun">
                            <svg class="c-stop-button__icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 66.46 66.46">
                                <rect id="stop_icon" data-name="stop icon" width="51.46" height="51.46" transform="translate(7.5 7.5)" fill="#fff" stroke-linejoin="round" stroke-width="15"/>
                            </svg>                              
                        </a>
                        <span class="c-play-button__text">STOP</span>
                </div>`
    },
    "simonsays": {
        "title": "Simon Says",
    },
    "tiktakboem": {
        "title": "Tik Tak Boem",
    },
    "colorhunt": {
        "title": "Color Hunt",
    },
    "speedrun-versus": {
        "title": "Speedrun Versus",
    },
    "simonsays-versus": {
        "title": "Simon Says Versus",
    }
}