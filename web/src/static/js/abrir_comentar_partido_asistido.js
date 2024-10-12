document.getElementById("botonComentarPartidoAsistido").addEventListener("click", function() {
    var contenedorComentarPartidoAsistido = document.getElementById("contenedorComentarPartidoAsistido");
    var contenedorBoton = document.getElementById("contenedorBoton");

    contenedorComentarPartidoAsistido.style.display = (contenedorComentarPartidoAsistido.style.display === "none") ? "block" : "none";

    if (contenedorComentarPartidoAsistido.style.display === "block") {
        contenedorComentarPartidoAsistido.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    contenedorBoton.style.display = "none";
});