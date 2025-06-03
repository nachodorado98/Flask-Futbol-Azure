function abrirVentanaEmergenteImagen() {
    document.getElementById("ventana-emergente-imagen").style.display = "block";
}

function cerrarVentanaEmergenteImagen() {
    document.getElementById("ventana-emergente-imagen").style.display = "none";
}

window.onclick = function(event) {
    const ventanaEmergente = document.getElementById("ventana-emergente-imagen");
    if (event.target == ventanaEmergente) {
        ventanaEmergente.style.display = "none";
    }
};