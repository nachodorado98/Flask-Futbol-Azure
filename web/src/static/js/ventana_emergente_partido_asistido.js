function abrirVentanaEmergenteTrayecto(trayecto) {

    let iconoTransporte = isNaN(trayecto[12]) ? trayecto[12] : trayecto[11];

    const html = `<h2 class="titulo-detalle-trayecto">Informacion del Trayecto de ${trayecto[15]}</h2>
                    <div class="contenedor-datos-on-tour-vuelta">
                        <img class="icono-distancia-on-tour-vuelta" src="/static/imagenes/iconos/cuentakilometros.png" alt="Distancia Icon">
                        <p class="distancia-on-tour-vuelta"><strong>Distancia: ${trayecto[16]} kilometros</strong></p>
                    </div>
                <div class="contenedor-pais-ciudad-partido">
                    <img src="/static/imagenes/iconos/${trayecto[13]}.png" alt="Icono Inicio" class="icono-tramo-trayecto-ida" />
                    <p class="texto-origen-destino-ida"><strong>${trayecto[3]}</strong></p>
                    <img src="/static/imagenes/iconos/linea_horizontal.png" alt="Línea horizontal" class="icono-flecha-derecha" />
                    <img src="/static/imagenes/iconos/${iconoTransporte}.png" alt="Icono Transporte" class="icono-transporte-ida" />
                    <img src="/static/imagenes/iconos/flecha_horizontal_derecha.png" alt="Flecha derecha" class="icono-flecha-derecha" />
                    <img src="/static/imagenes/iconos/${trayecto[14]}.png" alt="Icono Fin" class="icono-tramo-trayecto-ida" />
                    <p class="texto-origen-destino-ida"><strong>${trayecto[7]}</strong></p>
                </div>`;

    document.getElementById("contenido-ventana-trayecto").innerHTML = html;
    document.getElementById("ventana-emergente-trayecto").style.display = "block";
}

function cerrarVentanaEmergenteTrayecto() {
    document.getElementById("ventana-emergente-trayecto").style.display = "none";
}

window.onclick = function(event) {
    const ventanaEmergente = document.getElementById("ventana-emergente-trayecto");
    if (event.target == ventanaEmergente) {
        ventanaEmergente.style.display = "none";
    }
};

function abrirDesdeAtributo(elemento) {
    const trayecto = JSON.parse(elemento.dataset.trayecto);
    abrirVentanaEmergenteTrayecto(trayecto);
}