var batteries, battery_levels;

function mapp(x, in_min, in_max, out_min, out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

const handleBaterry = () => {
    for(const bat of batteries) {
        var percentage = 0
        currId = bat.getAttribute("tikid");
        //console.log(currId)

        battery_levels.forEach(function(bat) {
            if(bat.id == currId)percentage = bat.batt_level;
        })
        

        height = mapp(percentage, 0, 100, 0, 80);


        percentage<=20?fill='#e85856':percentage<=50?fill='#daa520':fill='#fff'

        bat.style.fill = fill;
        bat.style.transform = `translate(14.82px, ${100 - height}px)`;
        bat.style.height =  height + 'px';
        bat.parentNode.nextSibling.nextSibling.innerHTML = percentage + "%";
    }
}

const getBatteryLevels = async () => {
    battery_levels = await fetch(
        `http://${lanIP}/tiktem/v1/batteries`
    )
    .then((r) => (r.json()))
    .catch((err) => window.alert("Er is een probleem met de server"));
    console.log(battery_levels);

    handleBaterry();
}

const getBatteryDomElements = () => {
    batteries = document.querySelectorAll('.js-batery-state')
}

const initBattery = () => {
    console.log('Battery script loaded!')
    getBatteryDomElements();
    getBatteryLevels();
}

document.addEventListener('DOMContentLoaded', initBattery);