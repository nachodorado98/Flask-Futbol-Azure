function toggleMenu(menuId) {
    const allMenus = document.querySelectorAll(
        '.menu-desplegable-navbar-club, .menu-desplegable-navbar-estadios, .menu-desplegable-navbar-competiciones, .menu-desplegable-navbar-usuario, .menu-desplegable'
    );

    allMenus.forEach(menu => {
        if (menu.id !== menuId) {
            menu.style.display = "none";
        }
    });

    const currentMenu = document.getElementById(menuId);
    currentMenu.style.display = (currentMenu.style.display === "block") ? "none" : "block";
}

function desplegableNavBarClub() {
    toggleMenu('menuDesplegableNavBarClub');
}

function desplegableNavBarEstadios() {
    toggleMenu('menuDesplegableNavBarEstadios');
}

function desplegableNavBarCompeticiones() {
    toggleMenu('menuDesplegableNavBarCompeticiones');
}

function desplegableNavBarUsuario() {
    toggleMenu('menuDesplegableNavBarUsuario');
}

function desplegablePaises() {
    toggleMenu('menuDesplegable');
}

window.onclick = function(event) {
    const allMenus = document.querySelectorAll(
        '.menu-desplegable-navbar-club, .menu-desplegable-navbar-estadios, .menu-desplegable-navbar-competiciones, .menu-desplegable-navbar-usuario, .menu-desplegable'
    );

    if (!event.target.closest('.button-navbar-club') &&
        !event.target.closest('.menu-desplegable-navbar-club') &&
        !event.target.closest('.button-navbar-estadios') &&
        !event.target.closest('.menu-desplegable-navbar-estadios') &&
        !event.target.closest('.button-navbar-competiciones') &&
        !event.target.closest('.menu-desplegable-navbar-competiciones') &&
        !event.target.closest('.button-navbar-usuario') &&
        !event.target.closest('.menu-desplegable-navbar-usuario') &&
        !event.target.closest('.boton-desplegable') &&
        !event.target.closest('.menu-desplegable')) {
        allMenus.forEach(menu => menu.style.display = "none");
    }
};