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
                        <button class="o-button-reset c-play-button js-stop-button">
                            <svg class="c-stop-button__icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 66.46 66.46">
                                <rect class="c-stop-button__icon--rect" id="stop_icon" data-name="stop icon" width="51.46" height="51.46" transform="translate(7.5 7.5)" stroke-linejoin="round" stroke-width="15"/>
                            </svg>
                        </button>
                        <span class="c-play-button__text">STOP</span>
                </div>`,

        "htmlResult":`<div class="c-info-container u-mb-lg">
                            <h1 class="c-title">Results</h1>
                            <p class="c-info">
                                Je vervolledigde het parkour in
                            </p>
                        </div>
                        <p class="c-result__time js-score">0</p>`
               
    },
    "simonsays": {
        "title": "Simon Says",
        "id": 2,
        "html": `<div class="c-game-info-container">
                    <p class="c-game-info__header">Huidige reeks</p>
                    <p class="c-game-time__time js-score">0</p>
                </div>
                
                <div class="c-play-button-container">
                        <button class="o-button-reset c-play-button js-stop-button">
                            <svg class="c-stop-button__icon js-stop" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 66.46 66.46">
                                <rect class="c-stop-button__icon--rect" id="stop_icon" data-name="stop icon" width="51.46" height="51.46" transform="translate(7.5 7.5)" stroke-linejoin="round" stroke-width="15"/>
                            </svg>
                        </button>
                        <span class="c-play-button__text">STOP</span>
                </div>`,

        "htmlResult":`<div class="c-info-container u-mb-lg">
                            <h1 class="c-title">Results</h1>
                            <p class="c-info">
                                Je reeks was
                            </p>
                        </div>
                        <p class="c-result__time js-score">0</p>`

    },
    "tiktakboem": {
        "title": "Tik Tak Boem",
        
    },
    "colorhunt": {
        "title": "Color Hunt",
        "id": 4,
        "html": `<div class="c-game-info-container">
                    <p class="c-game-info__header">Huidige score</p>
                    <p class="c-game-time__time js-score">0</p>
                </div>
                
                <div class="c-play-button-container">
                        <button class="o-button-reset c-play-button js-stop-button">
                            <svg class="c-stop-button__icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 66.46 66.46">
                                <rect class="c-stop-button__icon--rect" id="stop_icon" data-name="stop icon" width="51.46" height="51.46" transform="translate(7.5 7.5)" stroke-linejoin="round" stroke-width="15"/>
                            </svg>
                        </button>
                        <span class="c-play-button__text">STOP</span>
                </div>`,

        "htmlResult":`<div class="c-info-container u-mb-lg">
                            <h1 class="c-title">Results</h1>
                            <p class="c-info">
                                Je eindscore was
                            </p>
                        </div>
                        <p class="c-result__time js-score">0</p>`
    },
    "speedrun-versus": {
        "title": "Speedrun Versus",
    },
    "simonsays-versus": {
        "title": "Simon Says Versus",
    }
}