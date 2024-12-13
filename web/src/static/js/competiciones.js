document.getElementById('competicion').addEventListener('change', function() {
    var valorSeleccionado = this.value;
    var urlActual = new URL(window.location.href);
    var params = new URLSearchParams(urlActual.search);

    if (valorSeleccionado) {
        params.set('competicion', valorSeleccionado);
    } else {
        params.delete('competicion');
    }

    window.location.href = urlActual.pathname + '?' + params.toString();
});