document.getElementById("boton-borrar-campos-on-tour").addEventListener("click", function () {
    var fechaIdaInput = document.getElementById("fecha-ida");
    var fechaVueltaInput = document.getElementById("fecha-vuelta");
    var transporteIdaInput = document.getElementById("transporte-ida");
    var transporteVueltaInput = document.getElementById("transporte-vuelta");

    fechaIdaInput.value = "";
    fechaVueltaInput.value = "";

    transporteIdaInput.selectedIndex = 0;
    transporteVueltaInput.selectedIndex = 0;

    var teletrabajoCheckbox = document.getElementById("teletrabajo");
    teletrabajoCheckbox.checked = false;

    console.log("Campos de fechas y checkbox de teletrabajo restablecidos.");
});