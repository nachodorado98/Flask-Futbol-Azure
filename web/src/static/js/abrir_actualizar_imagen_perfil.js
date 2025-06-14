document.getElementById("botonActualizarImagenPerfil").addEventListener("click", function() {
    var contenedorActualizarImagenPerfil = document.getElementById("contenedorActualizarImagenPerfil");
    var contenedorImagen = document.getElementById("contenedorImagen");

    contenedorActualizarImagenPerfil.style.display = (contenedorActualizarImagenPerfil.style.display === "none") ? "block" : "none";

    if (contenedorActualizarImagenPerfil.style.display === "block") {
        contenedorActualizarImagenPerfil.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

});