var countdownHTML, number = 5, countdownEnd = false;

const handleBaterry = () => {
}

const getCountdownDomElements = () => {
    countdownHTML = document.querySelector('.js-countdown');
}

const initBattery = () => {
    console.log('Countdown script loaded!')
    getBatteryDomElements();
    handleBaterry();
}

document.addEventListener('DOMContentLoaded', initBattery);