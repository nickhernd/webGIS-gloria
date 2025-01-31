// Variables globales para los gráficos
let waveChart = null;
let farmChart = null;

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar gráfico de oleaje
    initWaveChart();
});

// Inicializar gráfico principal de oleaje
function initWaveChart() {
    const ctx = document.getElementById('waveChart').getContext('2d');
    waveChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Altura de Olas (m)',
                data: [],
                borderColor: '#3b82f6',
                tension: 0.4,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Altura (m)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Hora'
                    }
                }
            }
        }
    });
}

// Inicializar gráfico específico de piscifactoría
function initFarmChart(canvasId) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    farmChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Altura de Olas',
                    data: [],
                    borderColor: '#3b82f6',
                    yAxisID: 'y1',
                },
                {
                    label: 'Temperatura',
                    data: [],
                    borderColor: '#ef4444',
                    yAxisID: 'y2',
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Altura (m)'
                    }
                },
                y2: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Temperatura (°C)'
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                }
            }
        }
    });
}

// Actualizar datos del gráfico de oleaje
async function updateWaveChart() {
    try {
        const response = await fetch('/api/wave-data');
        const data = await response.json();
        
        waveChart.data.labels = data.labels;
        waveChart.data.datasets[0].data = data.values;
        waveChart.update();
        
    } catch (error) {
        console.error('Error actualizando gráfico de oleaje:', error);
    }
}

// Actualizar datos del gráfico de piscifactoría
async function updateFarmChart(farmId) {
    try {
        const response = await fetch(`/api/farm-data/${farmId}`);
        const data = await response.json();
        
        if (!farmChart) {
            initFarmChart('farmChart');
        }
        
        farmChart.data.labels = data.labels;
        farmChart.data.datasets[0].data = data.waveHeight;
        farmChart.data.datasets[1].data = data.temperature;
        farmChart.update();
        
    } catch (error) {
        console.error('Error actualizando gráfico de piscifactoría:', error);
    }
}

// Destruir gráfico de piscifactoría
function destroyFarmChart() {
    if (farmChart) {
        farmChart.destroy();
        farmChart = null;
    }
}

// Actualizar todos los gráficos
function updateAllCharts() {
    updateWaveChart();
    // Si hay una piscifactoría seleccionada, actualizar su gráfico
    if (farmChart) {
        const farmId = farmChart.canvas.getAttribute('data-farm-id');
        if (farmId) {
            updateFarmChart(farmId);
        }
    }
}

// Iniciar actualizaciones periódicas
setInterval(updateAllCharts, 300000); // Actualizar cada 5 minutos

// Exportar funciones necesarias
window.chartManager = {
    updateWaveChart,
    updateFarmChart,
    destroyFarmChart
};
