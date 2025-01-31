
// Configuración de gráficos
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar gráfico de oleaje
    const waveCtx = document.getElementById('waveChart').getContext('2d');
    const waveChart = new Chart(waveCtx, {
        type: 'line',
        data: {
            labels: ['00:00', '03:00', '06:00', '09:00', '12:00'],
            datasets: [{
                label: 'Altura de Olas (m)',
                data: [1.2, 1.5, 1.8, 1.6, 1.4],
                borderColor: 'rgb(59, 130, 246)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });

    // Actualizar datos meteorológicos
    function updateWeatherData(data = null) {
        // Datos de ejemplo (reemplazar con datos reales de la API)
        const weatherData = data || {
            temperatura: '22°C',
            viento: '15 km/h',
            humedad: '75%'
        };

        const weatherContainer = document.getElementById('weather-data');
        weatherContainer.innerHTML = `
            <div class="flex justify-between items-center">
                <span class="text-gray-600">Temperatura</span>
                <span class="font-semibold">${weatherData.temperatura}</span>
            </div>
            <div class="flex justify-between items-center">
                <span class="text-gray-600">Viento</span>
                <span class="font-semibold">${weatherData.viento}</span>
            </div>
            <div class="flex justify-between items-center">
                <span class="text-gray-600">Humedad</span>
                <span class="font-semibold">${weatherData.humedad}</span>
            </div>
        `;
    }

    // Actualizar alertas
    function updateAlerts(alerts = null) {
        // Alertas de ejemplo (reemplazar con datos reales)
        const alertsList = alerts || [
            {
                tipo: 'warning',
                mensaje: 'Altura de olas superior a 2m prevista para mañana'
            },
            {
                tipo: 'info',
                mensaje: 'Actualización de datos Copernicus completada'
            }
        ];

        const alertsContainer = document.getElementById('alerts-container');
        alertsContainer.innerHTML = alertsList.map(alert => `
            <div class="bg-${alert.tipo === 'warning' ? 'yellow' : 'blue'}-50 p-4 rounded-md">
                <p class="text-${alert.tipo === 'warning' ? 'yellow' : 'blue'}-800">
                    ${alert.mensaje}
                </p>
            </div>
        `).join('');
    }

    // Actualizar estado del pipeline
    function updatePipelineStatus(status = 'running') {
        const statusElement = document.getElementById('pipeline-status');
        const isRunning = status === 'running';
        
        statusElement.className = `ml-2 px-2 py-1 rounded-full text-sm ${
            isRunning ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
        }`;
        statusElement.textContent = isRunning ? 'En ejecución' : 'Detenido';
    }

    // Función para actualizar los datos del oleaje
    function updateWaveData(data = null) {
        const newData = data || {
            labels: ['00:00', '03:00', '06:00', '09:00', '12:00'],
            values: [1.2, 1.5, 1.8, 1.6, 1.4]
        };

        waveChart.data.labels = newData.labels;
        waveChart.data.datasets[0].data = newData.values;
        waveChart.update();
    }

    // Inicializar datos
    updateWeatherData();
    updateAlerts();
    updatePipelineStatus();

    // Configurar actualizaciones periódicas
    setInterval(() => {
        // Aquí irían las llamadas a la API para obtener datos actualizados
        fetch('/api/wave-data')
            .then(response => response.json())
            .then(data => updateWaveData(data))
            .catch(console.error);

        fetch('/api/weather-data')
            .then(response => response.json())
            .then(data => updateWeatherData(data))
            .catch(console.error);

        fetch('/api/alerts')
            .then(response => response.json())
            .then(data => updateAlerts(data))
            .catch(console.error);

        fetch('/api/pipeline-status')
            .then(response => response.json())
            .then(data => updatePipelineStatus(data.status))
            .catch(console.error);
    }, 30000); // Actualizar cada 30 segundos
});
