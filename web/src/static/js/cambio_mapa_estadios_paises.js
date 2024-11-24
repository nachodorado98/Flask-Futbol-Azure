function cambiarMapa(urlMapa, boton) {
    const iframe = document.getElementById('iframe-mapa');

    iframe.classList.add('hidden');
    
    setTimeout(() => {
        iframe.src = urlMapa;
        iframe.classList.remove('hidden');
    }, 300);

    const botones = document.querySelectorAll('.botones-mapa-detalle button');
    botones.forEach(b => b.classList.remove('active'));
    boton.classList.add('active');
}