document.addEventListener("DOMContentLoaded", function() {
    const golesLocal = document.getElementById("goles_local");
    const golesVisitante = document.getElementById("goles_visitante");
    const contenedorGoleadores = document.getElementById("goleadores-container");
    const divLocal = document.getElementById("goleadores-local");
    const divVisitante = document.getElementById("goleadores-visitante");

    const porraData = document.getElementById("porra-data");
    const nombreLocal = porraData ? porraData.dataset.local : "Local";
    const nombreVisitante = porraData ? porraData.dataset.visitante : "Visitante";

    const jugadoresLocal = window.jugadoresLocal || [];
    const jugadoresVisitante = window.jugadoresVisitante || [];
    const urlImagenJugador = window.urlImagenJugador || '/static/';

    function generarSelects(div, goles, jugadores, titulo) {
        const lista = div.querySelector(".lista-goleadores");
        if (!lista) return;
        lista.innerHTML = "";

        for (let i = 0; i < goles; i++) {
            const select = document.createElement("select");

            const equipoSlug = titulo.toLowerCase().includes(nombreLocal.toLowerCase())
                ? 'local'
                : 'visitante';

            select.name = `${equipoSlug}_goleador_${i + 1}`;
            select.required = true;
            select.classList.add('select-goleador');

            const optionDefault = document.createElement("option");
            optionDefault.value = "";
            optionDefault.textContent = "Selecciona goleador";
            optionDefault.disabled = true;
            optionDefault.selected = true;
            select.appendChild(optionDefault);

            jugadores.forEach(j => {
                let id, nombre, imagen;

                if (Array.isArray(j)) {
                    id = j[0];
                    nombre = j[1];
                    imagen = j[2] !== undefined ? j[2] : null;
                } else if (typeof j === 'object' && j !== null) {
                    id = j.id ?? j[0];
                    nombre = j.nombre ?? j[1];
                    imagen = j.imagen ?? j[2] ?? null;
                } else {
                    id = j;
                    nombre = String(j);
                    imagen = null;
                }

                const opt = document.createElement("option");
                opt.value = id;
                opt.textContent = nombre;

                if (imagen === undefined || imagen === null || imagen === "-1") {
                    opt.dataset.img = "/static/imagenes/iconos/no_jugador.png";
                } else {
                    if (
                        imagen.startsWith("http://") ||
                        imagen.startsWith("https://") ||
                        imagen.startsWith("/")
                    ) {
                        opt.dataset.img = imagen;
                    } else {
                        opt.dataset.img = urlImagenJugador + imagen + ".png";
                    }
                }

                select.appendChild(opt);
            });

            lista.appendChild(select);
        }

        aplicarImagenesSelect();
    }

    function aplicarImagenesSelect() {
        document.querySelectorAll(".equipo-goleadores select.select-goleador").forEach(select => {
            const aplicarFondo = el => {
                const selectedOption = el.options[el.selectedIndex];
                const img = selectedOption ? selectedOption.dataset.img : null;
                if (img) {
                    el.style.backgroundImage = `url('${img}')`;
                    el.style.backgroundRepeat = "no-repeat";
                    el.style.backgroundPosition = "8px center";
                    el.style.backgroundSize = "30px 30px";
                    el.style.paddingLeft = "45px";
                } else {
                    el.style.backgroundImage = "none";
                    el.style.paddingLeft = "8px";
                }
            };

            aplicarFondo(select);

            select.removeEventListener("change", select._changeHandler || (() => {}));
            const handler = function() {
                aplicarFondo(this);
            };
            select.addEventListener("change", handler);
            select._changeHandler = handler;
        });
    }

    function actualizarGoleadores() {
        const gL = parseInt(golesLocal.value);
        const gV = parseInt(golesVisitante.value);

        if (!isNaN(gL) && !isNaN(gV)) {
            contenedorGoleadores.classList.remove("oculto");

            generarSelects(divLocal, gL, jugadoresLocal, `Goleadores del ${nombreLocal}`);
            generarSelects(divVisitante, gV, jugadoresVisitante, `Goleadores del ${nombreVisitante}`);
        } else {
            contenedorGoleadores.classList.add("oculto");

            const listaLocal = divLocal.querySelector(".lista-goleadores");
            const listaVisitante = divVisitante.querySelector(".lista-goleadores");
            if (listaLocal) listaLocal.innerHTML = "";
            if (listaVisitante) listaVisitante.innerHTML = "";
        }
    }

    golesLocal.addEventListener("input", actualizarGoleadores);
    golesVisitante.addEventListener("input", actualizarGoleadores);

    if (golesLocal.value !== "" && golesVisitante.value !== "") {
        actualizarGoleadores();
    }
});