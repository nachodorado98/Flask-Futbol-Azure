document.querySelectorAll('.tipo-partidos').forEach(function(enlace) {
    enlace.addEventListener('click', function(event) {
        event.preventDefault();

        var localValue = enlace.getAttribute('data-local');
        var urlActual = new URL(window.location.href);
        var params = new URLSearchParams(urlActual.search);

        if (localValue) {
            params.set('local', localValue);
        } else {
            params.delete('local');
        }

        window.location.href = urlActual.pathname + '?' + params.toString();
    });
});