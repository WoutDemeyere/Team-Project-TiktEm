var batteries;

function mapp(x, in_min, in_max, out_min, out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

const tempStatus = {
    0 : 100,
    1 : 60,
    2 : 21,
    3 : 10
}

const handleBaterry = () => {
    for(const bat of batteries) {
        currId = bat.getAttribute("tikid");
        percentage = tempStatus[currId]
        height = mapp(percentage, 0, 100, 0, 80);

        console.log(100-height);

        percentage<=20?fill='#e85856':percentage<=50?fill='#daa520':fill='#fff'

        bat.style.fill = fill;
        bat.style.transform = `translate(14.82px, ${100 - height}px)`;
        bat.style.height =  height + 'px';
        bat.parentNode.nextSibling.nextSibling.innerHTML = percentage + "%";
    }
}

const getBatteryDomElements = () => {
    batteries = document.querySelectorAll('.js-batery-state')
}

const initBattery = () => {
    console.log('Battery script loaded!')
    getBatteryDomElements();
    handleBaterry();
}

document.addEventListener('DOMContentLoaded', initBattery);