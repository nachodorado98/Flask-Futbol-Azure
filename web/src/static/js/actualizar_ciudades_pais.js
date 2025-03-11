function actualizarCiudades() {
    var paisSeleccionado = document.getElementById("pais").value;
    var ciudadDropdown = document.getElementById("ciudad");

    while (ciudadDropdown.options.length > 0) {
        ciudadDropdown.remove(0);
    }

    if (paisSeleccionado) {

        fetch("/ciudades_pais?pais=" + encodeURIComponent(paisSeleccionado))
            .then(response => response.json())
            .then(ciudades => {

                ciudades.forEach(function(ciudad) {
                    var option = document.createElement("option");
                    option.text = ciudad;
                    option.value = ciudad;
                    ciudadDropdown.add(option);
                });
            })
            .catch(error => console.error("Error al obtener ciudades:", error));
    }
}

function actualizarCiudadesEspecificas(paisSelectId, ciudadSelectId) {
    var paisSeleccionado = document.getElementById(paisSelectId).value;
    var ciudadDropdown = document.getElementById(ciudadSelectId);

    while (ciudadDropdown.options.length > 0) {
        ciudadDropdown.remove(0);
    }

    if (paisSeleccionado) {

        fetch("/ciudades_pais?pais=" + encodeURIComponent(paisSeleccionado))
            .then(response => response.json())
            .then(ciudades => {

                ciudades.forEach(function(ciudad) {
                    var option = document.createElement("option");
                    option.text = ciudad;
                    option.value = ciudad;
                    ciudadDropdown.add(option);
                });
            })
            .catch(error => console.error("Error al obtener ciudades:", error));
    }
}