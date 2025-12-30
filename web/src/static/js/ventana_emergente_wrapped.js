function abrirVentana(idVentana) {
    document.getElementById(idVentana).style.display = "block";
}

function cerrarVentana(idVentana) {
    document.getElementById(idVentana).style.display = "none";
}

window.onclick = function (event) {
    if (event.target.classList.contains("ventana-emergente")) {
        event.target.style.display = "none";
    }
};