// Clase para gestionar datos meteorológicos
class WeatherManager {
    constructor() {
        this.weatherData = {};
        this.updateInterval = 900000; // 15 minutos
        this.init();
    }

    init() {
        // Iniciar actualizaciones periódicas
        this.updateWeather();
        setInterval(() => this.updateWeather(), this.updateInterval);
    }

    async updateWeather() {
        try {
            const response = await fetch('/api/weather-data');
            const data = await response.json();
            this.weatherData = data;
            this.updateUI();
        } catch (error) {
            console.error('Error actualizando datos meteorológicos:', error);
            window.mapManager?.showAlert('Error al actualizar datos meteorológicos', 'error');
        }
    }

    updateUI() {
        // Actualizar elementos del DOM
        document.getElementById('temp-value').textContent = 
            `${this.weatherData.temperature?.toFixed(1)}°C`;
        document.getElementById('wind-value').textContent = 
            `${this.weatherData.windSpeed?.toFixed(1)} km/h`;
        document.getElementById('humidity-value').textContent = 
            `${this.weatherData.humidity?.toFixed(0)}%`;

        // Actualizar otros indicadores meteorológicos si existen
        this.updateWeatherIndicators();
    }

    updateWeatherIndicators() {
        // Actualizar indicadores visuales de condiciones meteorológicas
        const weatherCard = document.querySelector('.weather-card');
        if (!weatherCard) return;

        // Limpiar indicadores existentes
        const oldIndicators = weatherCard.querySelector('.weather-indicators');
        if (oldIndicators) oldIndicators.remove();

        // Crear nuevos indicadores
        const indicators = document.createElement('div');
        indicators.className = 'weather-indicators';
        
        // Añadir indicador de condición actual
        if (this.weatherData.condition) {
            const conditionDiv = document.createElement('div');
            conditionDiv.className = 'weather-condition';
            conditionDiv.innerHTML = `
                <img src="/images/weather/${this.weatherData.condition}.svg" 
                     alt="${this.weatherData.condition}" 
                     class="weather-icon" />
                <span>${this.getConditionText(this.weatherData.condition)}</span>
            `;
            indicators.appendChild(conditionDiv);
        }

        // Añadir indicador de alertas si existen
        if (this.weatherData.alerts && this.weatherData.alerts.length > 0) {
            const alertsDiv = document.createElement('div');
            alertsDiv.className = 'weather-alerts';
            alertsDiv.innerHTML = this.weatherData.alerts
                .map(alert => `<div class="weather-alert ${alert.severity}">${alert.message}</div>`)
                .join('');
            indicators.appendChild(alertsDiv);
        }

        weatherCard.appendChild(indicators);
    }

    getConditionText(condition) {
        const conditions = {
            clear: 'Despejado',
            cloudy: 'Nublado',
            rain: 'Lluvia',
            storm: 'Tormenta',
            snow: 'Nieve',
            fog: 'Niebla'
        };
        return conditions[condition] || condition;
    }

    // Métodos para acceder a los datos
    getTemperature() {
        return this.weatherData.temperature;
    }

    getWindSpeed() {
        return this.weatherData.windSpeed;
    }

    getHumidity() {
        return this.weatherData.humidity;
    }

    getAlerts() {
        return this.weatherData.alerts || [];
    }

    // Método para comprobar condiciones peligrosas
    checkDangerousConditions() {
        const dangerous = [];

        if (this.weatherData.windSpeed > 50) {
            dangerous.push({
                type: 'wind',
                message: 'Vientos fuertes detectados',
                severity: 'high'
            });
        }

        if (this.weatherData.waveHeight > 3) {
            dangerous.push({
                type: 'waves',
                message: 'Altura de olas peligrosa',
                severity: 'high'
            });
        }

        return dangerous;
    }
}

// Crear instancia global
window.weatherManager = new WeatherManager();

// Exportar para uso en otros módulos
export default WeatherManager;
