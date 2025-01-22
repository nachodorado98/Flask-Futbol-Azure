document.getElementById("botonOnTourPartidoAsistido").addEventListener("click", function() {
    var contenedorOnTourPartidoAsistido = document.getElementById("contenedorOnTourPartidoAsistido");
    var contenedorOnTour = document.getElementById("contenedorOnTour");

    contenedorOnTourPartidoAsistido.style.display = (contenedorOnTourPartidoAsistido.style.display === "none") ? "block" : "none";

    if (contenedorOnTourPartidoAsistido.style.display === "block") {
        contenedorOnTourPartidoAsistido.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    contenedorOnTour.style.display = "none";
});