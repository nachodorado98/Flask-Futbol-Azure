function actualizarFechasPartidoAsistido() {

    var partidoSeleccionado = document.getElementById("partido_anadir").value;

    var fechaIdaInput = document.getElementById("fecha-ida");
    var fechaVueltaInput = document.getElementById("fecha-vuelta");

    fechaIdaInput.value = "";
    fechaVueltaInput.value = "";

    if (partidoSeleccionado && partidoSeleccionado !== "sin-seleccion") {

        fetch("/fecha_partido?partido_id=" + encodeURIComponent(partidoSeleccionado))
            .then(response => response.json())
            .then(fechaPartido => {
                if (fechaPartido) {
                    var fechaPartidoISO = new Date(fechaPartido.fecha_ida).toISOString().split("T")[0];

                    var fechaIdaInput = document.getElementById("fecha-ida");
                    fechaIdaInput.max = fechaPartidoISO;

                    var fechaVueltaInput = document.getElementById("fecha-vuelta");
                    fechaVueltaInput.min = fechaPartidoISO;
                } else {
                    console.error("No se recibieron fechas para el partido seleccionado.");
                }
            })
            .catch(error => console.error("Error al obtener fechas del partido:", error));
    } else {
        document.getElementById("fecha-ida").removeAttribute("max");
        document.getElementById("fecha-vuelta").removeAttribute("min");
    }
}