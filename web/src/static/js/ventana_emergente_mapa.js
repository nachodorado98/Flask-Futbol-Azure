function abrirVentanaEmergenteMapa() {
    document.getElementById("ventana-emergente-mapa").style.display = "block";
}

function cerrarVentanaEmergenteMapa() {
    document.getElementById("ventana-emergente-mapa").style.display = "none";
}

window.onclick = function(event) {
    const ventanaEmergente = document.getElementById("ventana-emergente-mapa");
    if (event.target == ventanaEmergente) {
        ventanaEmergente.style.display = "none";
    }
};