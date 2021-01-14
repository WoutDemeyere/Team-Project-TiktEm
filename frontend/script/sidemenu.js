var sideOpen, sideClose, sideMenu;

const listenToSideNavButtons = () => {
    sideOpen.addEventListener('click', function () {
        sideMenu.style.width = "85%" 
        handleNavItems();
    });

    sideClose.addEventListener('click', function () {
        sideMenu.style.width = "0" 
    });
}

const handleNavItems = function () {
    for (const nav of navs) {
        nav.addEventListener('click', function () {
            for (const nav of navs) {
                nav.classList.remove('c-nav-is-selected')
            }
            nav.classList.add('c-nav-is-selected')
        });
    }
}

const getDomElements = () => {
    sideOpen = document.querySelector('.js-sidenav-open');
    sideClose = document.querySelector('.js-sidenav-close');
    sideMenu = document.querySelector('.js-side-menu')
    navs = document.querySelectorAll('.js-nav-item');
}

const init = () => {
    console.log('Sidemenu script loaded!')
    getDomElements();
    listenToSideNavButtons();
}

document.addEventListener('DOMContentLoaded', init);