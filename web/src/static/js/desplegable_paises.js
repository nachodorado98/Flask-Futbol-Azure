function desplegablePaises() {
    const menu = document.getElementById("menuDesplegable");
    menu.style.display = (menu.style.display === "block") ? "none" : "block";
}

window.onclick = function(event) {

    if (!event.target.matches('.boton-desplegable, .boton-desplegable *')) {
        const menu = document.getElementById("menuDesplegable");

        if (menu.style.display === "block") {
            menu.style.display = "none";
        }
    }
}