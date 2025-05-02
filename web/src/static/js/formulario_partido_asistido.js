function manejarCambioPartido() {

    var partidoSeleccionado = document.getElementById("partido_anadir").value;

    var fechaIdaInput = document.getElementById("fecha-ida");
    var fechaVueltaInput = document.getElementById("fecha-vuelta");
    var estadioIdaSelect = document.getElementById("ciudad-ida-estadio");
    var estadioVueltaSelect = document.getElementById("ciudad-vuelta-estadio");

    fechaIdaInput.value = "";
    fechaVueltaInput.value = "";
    estadioIdaSelect.innerHTML = "";
    estadioVueltaSelect.innerHTML = "";

    if (partidoSeleccionado && partidoSeleccionado !== "sin-seleccion") {

        fetch("/fecha_partido?partido_id=" + encodeURIComponent(partidoSeleccionado))
            .then(response => response.json())
            .then(fechaPartido => {

                if (fechaPartido) {
                    var fechaPartidoISO = new Date(fechaPartido.fecha_ida).toISOString().split("T")[0];

                    fechaIdaInput.max = fechaPartidoISO;
                    fechaVueltaInput.min = fechaPartidoISO;

                } else {
                    console.error("No se recibieron fechas para el partido seleccionado.");
                }
            })
            .catch(error => console.error("Error al obtener fechas del partido:", error));

        fetch("/estadio_partido?partido_id=" + encodeURIComponent(partidoSeleccionado))
            .then(response => response.json())
            .then(data => {
                if (data && data.estadio && Array.isArray(data.estadio) && data.estadio.length >= 2) {

                    var estadioIdaValue = data.estadio[0];
                    var estadioIdaTexto = data.estadio[1];

                    var optionIda = document.createElement("option");
                    optionIda.value = estadioIdaValue;
                    optionIda.textContent = estadioIdaTexto;
                    optionIda.selected = true;

                    estadioIdaSelect.appendChild(optionIda);

                    var estadioVueltaValue = data.estadio[0];
                    var estadioVueltaTexto = data.estadio[1];

                    var optionVuelta = document.createElement("option");
                    optionVuelta.value = estadioVueltaValue;
                    optionVuelta.textContent = estadioVueltaTexto;

                    estadioVueltaSelect.appendChild(optionVuelta);

                } else {
                    console.error("Formato de estadio incorrecto o datos no válidos:", data);
                }
            })
            .catch(error => console.error("Error al obtener el estadio del partido:", error));
    } else {
        fechaIdaInput.removeAttribute("max");
        fechaVueltaInput.removeAttribute("min");
    }
}