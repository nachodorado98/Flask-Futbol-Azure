function estadiosTopFiltro() {
    const select = document.getElementById('cantidad-estadios-select');
    const valorSeleccionado = select.value;
    window.location.href = `/estadios?top_estadios=${valorSeleccionado}`;
}
