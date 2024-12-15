document.getElementById('resultados').addEventListener('change', function() {
    var valorSeleccionado = this.value;
    var urlActual = new URL(window.location.href);
    var params = new URLSearchParams(urlActual.search);

    if (valorSeleccionado) {
        params.set('resultados', valorSeleccionado);
    } else {
        params.delete('resultados');
    }

    window.location.href = urlActual.pathname + '?' + params.toString();
});