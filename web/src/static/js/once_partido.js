function cambiarEquipo(tipo) {
    equipoActual = tipo;
    pintar();
    marcarEscudo();
}

function pintar() {
    pintarEntrenador();
    pintarJugadores();
}

function pintarEntrenador() {
    const e = entrenadores[equipoActual === "local" ? 0 : 1];

    document.getElementById("entrenador").innerHTML = `
        <div class="info-entrenador-partido"
             onclick="window.location.href='/entrenador/${e[0]}'">

            <img class="equipo-entrenador-partido"
                 src="${e[5] == -1 ? '/static/imagenes/iconos/no_escudo.png' : urlEscudo + e[5] + '.png'}">

            <img class="entrenador-partido"
                 src="${e[2] == '-1' ? '/static/imagenes/iconos/no_entrenador.png' : urlEntrenador + e[2] + '.png'}">

            <h4>${e[1]}</h4>

            <img src="/static/imagenes/iconos/tactica.png" class="tactica-imagen" alt="Tactica Icon">

            <h4>${e[3]}</h4>
        </div>
    `;
}

function pintarJugadores() {
    const cont = document.getElementById("jugadores");
    cont.innerHTML = "";

    jugadores[equipoActual].forEach(j => {
        cont.innerHTML += `
            <div class="tarjeta-jugador-partido"
                 onclick="window.location.href='/jugador/${j[0]}'">

                <div class="info-jugador-partido">

                    <img class="equipo-jugador-partido"
                         src="${j[4] == -1 ? '/static/imagenes/iconos/no_escudo.png' : urlEscudo + j[4] + '.png'}">

                    <img class="jugador-partido"
                         src="${j[2] == '-1' ? '/static/imagenes/iconos/no_jugador.png' : urlJugador + j[2] + '.png'}">

                    <h4>${j[1]}</h4>

                    <img class="camiseta-icon" src="/static/imagenes/iconos/camiseta.png">

                    <h4>${j[5]}</h4>

                </div>
            </div>
        `;
    });
}

function marcarEscudo() {
    document.querySelectorAll(".escudo-alineacion").forEach(e => {
        e.classList.toggle(
            "activo",
            e.dataset.equipo === equipoActual
        );
    });
}

document.addEventListener("DOMContentLoaded", pintar);