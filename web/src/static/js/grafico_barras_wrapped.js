document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById("grafico_barras");
    var ctx = canvas.getContext("2d");
    var barraColor = getComputedStyle(canvas).getPropertyValue('--color-secundario') || "rgba(255, 132, 132, 0.5)";

    var myChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: datos_grafica_barras.meses,
            datasets: [{
                label: "Partidos por Mes",
                data: datos_grafica_barras.num_partidos,
                backgroundColor: barraColor,
                borderColor: barraColor,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,

            onHover: function (event, chartElement) {
                event.native.target.style.cursor = chartElement[0] ? "pointer" : "default";
            },

            // 👉 CLICK EN BARRA
            onClick: function (evt, elements) {

                if (!elements.length) return;

                const index = elements[0].index;

                const mes = datos_grafica_barras.meses[index];

                const partidosMes = datos_grafica_barras.partidos[mes];

                // ⭐ título dinámico
                document.getElementById("titulo-ventana-mes").innerHTML =
                    `<strong>Partidos Asistidos ${mes}</strong>`;

                const contenedor = document.getElementById("lista-partidos-por-mes");
                contenedor.innerHTML = "";

                if (!partidosMes || partidosMes.length === 0) {

                    contenedor.innerHTML = `<p>No hay partidos en ${mes}</p>`;

                } else {

                    partidosMes.forEach(function (partido) {

                        const id = partido[0];

                        const tarjeta = document.createElement("div");
                        tarjeta.className = "tarjeta-partido-asistidos";
                        tarjeta.onclick = function () {
                            window.location.href = "/partido/" + id + "/asistido";
                        };

                        tarjeta.innerHTML = `
                            <p><strong>${partido[2]} - ${partido[3]}</strong></p>
                            <div class="info-partido-asistidos">
                                <img src="${partido[4] === -1 ? '/static/imagenes/iconos/no_escudo.png' : url_imagen_escudo + partido[4] + '.png'}" alt="Local Icon">

                                <h4>${partido[6]} ${partido[1]} ${partido[7]}</h4>

                                <img src="${partido[5] === -1 ? '/static/imagenes/iconos/no_escudo.png' : url_imagen_escudo + partido[5] + '.png'}" alt="Visitante Icon">
                            </div>
                        `;

                        contenedor.appendChild(tarjeta);
                    });

                }

                // 👉 abrir ventana del mes
                abrirVentana('ventana-emergente-mes');
            },

            plugins: {
                legend: { display: false }
            },

            scales: {
                x: {
                    ticks: { color: "#ffffff", font: { size: 14 } },
                    grid: { display: false }
                },
                y: {
                    beginAtZero: true,
                    ticks: { color: "#ffffff", font: { size: 14 }, precision: 0 },
                    grid: { display: false }
                }
            }
        }
    });
});
