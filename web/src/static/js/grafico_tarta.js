document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById("grafico_tarta").getContext("2d");
    
    var myPieChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["Ganados", "Empatados", "Perdidos"],
            datasets: [{
                label: "Resultados de Partidos",
                data: [datos_grafica_tarta.ganados, datos_grafica_tarta.empatados, datos_grafica_tarta.perdidos],
                backgroundColor: [
                    "rgba(58, 224, 5, 0.7)",
                    "rgba(255, 165, 0, 0.7)",
                    "rgba(255, 0, 0, 0.7)"
                ],
                borderColor: [
                    "rgba(58, 224, 5, 1)",
                    "rgba(255, 165, 0, 1)",
                    "rgba(255, 0, 0, 1)"
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display:false
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            var label = tooltipItem.label || '';
                            var value = tooltipItem.raw;
                            return `${value} partidos`;
                        }
                    }
                }
            }
        }
    });
});
