function redireccionarConValor(event) {
    event.preventDefault();

    const partidoId = document.getElementById('seleccion-partido-favorito').value;

    if (partidoId) {
        const url = `/partido/${partidoId}/asistido/anadir_partido_favorito`;
        
        window.location.href = url;
    } else {
        alert("Por favor, selecciona un partido.");
    }
}