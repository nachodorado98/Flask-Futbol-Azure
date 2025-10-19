document.addEventListener("DOMContentLoaded", function() {
    const golesLocal = document.getElementById("goles_local");
    const golesVisitante = document.getElementById("goles_visitante");
    const contenedorGoleadores = document.getElementById("goleadores-container");
    const divLocal = document.getElementById("goleadores-local");
    const divVisitante = document.getElementById("goleadores-visitante");

    const porraData = document.getElementById("porra-data");
    const nombreLocal = porraData.dataset.local;
    const nombreVisitante = porraData.dataset.visitante;

    const jugadoresLocal = window.jugadoresLocal || [];
    const jugadoresVisitante = window.jugadoresVisitante || [];

    function generarSelects(div, goles, equipo, titulo, jugadores) {
        div.innerHTML = `<p>${titulo}</p>`;
        for (let i = 0; i < goles; i++) {
            const select = document.createElement("select");
            select.name = `${equipo.toLowerCase()}_goleador_${i+1}`;
            select.required = true;

            const optionDefault = document.createElement("option");
            optionDefault.value = "";
            optionDefault.textContent = `Selecciona goleador`;
            optionDefault.disabled = true;
            optionDefault.selected = true;
            select.appendChild(optionDefault);


            jugadores.forEach(jugador => {
                const opt = document.createElement("option");
                opt.value = jugador.id;
                opt.textContent = jugador.nombre;
                select.appendChild(opt);
            });

            div.appendChild(select);
        }
    }

    function actualizarGoleadores() {
        const gL = parseInt(golesLocal.value);
        const gV = parseInt(golesVisitante.value);

        if (!isNaN(gL) && !isNaN(gV)) {
            contenedorGoleadores.classList.remove("oculto");

            generarSelects(divLocal, gL, nombreLocal, `Goleadores del ${nombreLocal}`, jugadoresLocal);
            generarSelects(divVisitante, gV, nombreVisitante, `Goleadores del ${nombreVisitante}`, jugadoresVisitante);
        } else {
            contenedorGoleadores.classList.add("oculto");
            divLocal.innerHTML = `<p>Goleadores del ${nombreLocal}</p>`;
            divVisitante.innerHTML = `<p>Goleadores del ${nombreVisitante}</p>`;
        }
    }

    golesLocal.addEventListener("input", actualizarGoleadores);
    golesVisitante.addEventListener("input", actualizarGoleadores);
});