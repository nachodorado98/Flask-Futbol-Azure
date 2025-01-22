document.getElementById("botonNoOnTourPartidoAsistido").addEventListener("click", function() {
    var contenedorOnTourPartidoAsistido = document.getElementById("contenedorOnTourPartidoAsistido");
    var contenedorOnTour = document.getElementById("contenedorOnTour");

    contenedorOnTourPartidoAsistido.style.display = "none";
    contenedorOnTour.style.display = "flex";
});