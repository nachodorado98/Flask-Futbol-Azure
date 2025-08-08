function cerrarVentanaEmergentePartidoLogin() {
    document.getElementById("ventana-emergente-partido-login").style.display = "none";
}

window.onclick = function(event) {
    const ventanaEmergente = document.getElementById("ventana-emergente-partido-login");
    if (event.target == ventanaEmergente) {
        ventanaEmergente.style.display = "none";
    }
};