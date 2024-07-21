document.getElementById('temporada').addEventListener('change', function() {
    var valorSeleccionado = this.value;
    var urlActual = new URL(window.location.href);
    var params = new URLSearchParams(urlActual.search);

    if (valorSeleccionado) {
        params.set('temporada', valorSeleccionado);
    } else {
        params.delete('temporada');
    }

    window.location.href = urlActual.pathname + '?' + params.toString();
});

document.querySelectorAll('.contenedor-tipo-partidos a').forEach(function(enlace) {
    enlace.addEventListener('click', function(event) {
        var urlActual = new URL(window.location.href);
        var params = new URLSearchParams(urlActual.search);
        var temporada = params.get('temporada');

        if (temporada) {
            var urlEnlace = new URL(enlace.href);
            var paramsEnlace = new URLSearchParams(urlEnlace.search);
            paramsEnlace.set('temporada', temporada);
            enlace.href = urlEnlace.pathname + '?' + paramsEnlace.toString();
        }
    });
});