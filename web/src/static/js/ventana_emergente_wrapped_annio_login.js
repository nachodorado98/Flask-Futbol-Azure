function cerrarVentanaEmergenteWrappedAnnioLogin() {
    document.getElementById("ventana-emergente-wrapped-annio-login").style.display = "none";
}

window.onclick = function(event) {
    const ventanaEmergente = document.getElementById("ventana-emergente-wrapped-annio-login");
    if (event.target == ventanaEmergente) {
        ventanaEmergente.style.display = "none";
    }
};