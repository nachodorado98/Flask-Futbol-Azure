function abrirVentanaEmergente() {
    document.getElementById("ventana-emergente").style.display = "block";
}

function cerrarVentanaEmergente() {
    document.getElementById("ventana-emergente").style.display = "none";
}

window.onclick = function(event) {
    const ventanaEmergente = document.getElementById("ventana-emergente");
    if (event.target == ventanaEmergente) {
        ventanaEmergente.style.display = "none";
    }
};