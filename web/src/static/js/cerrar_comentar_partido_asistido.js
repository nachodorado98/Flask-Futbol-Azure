document.getElementById("botonNoComentarPartidoAsistido").addEventListener("click", function() {
    var contenedorComentarPartidoAsistido = document.getElementById("contenedorComentarPartidoAsistido");
    var contenedorBoton = document.getElementById("contenedorBoton");

    contenedorComentarPartidoAsistido.style.display = "none";
    contenedorBoton.style.display = "block";
});