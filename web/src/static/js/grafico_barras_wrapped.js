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
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: "#ffffff",
                        font: { size: 14 }
                    },
                    grid: { display: false }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: "#ffffff",
                        font: { size: 14 },
                        precision: 0
                    },
                    grid: { display: false }
                }
            }
        }
    });
});