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