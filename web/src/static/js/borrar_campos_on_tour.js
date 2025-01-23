document.getElementById("boton-borrar-campos-on-tour").addEventListener("click", function () {
    var fechaIdaInput = document.getElementById("fecha-ida");
    var fechaVueltaInput = document.getElementById("fecha-vuelta");

    fechaIdaInput.value = "";
    fechaVueltaInput.value = "";

    var teletrabajoCheckbox = document.getElementById("teletrabajo");
    teletrabajoCheckbox.checked = false;

    console.log("Campos de fechas y checkbox de teletrabajo restablecidos.");
});