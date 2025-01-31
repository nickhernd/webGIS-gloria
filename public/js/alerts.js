// Clase para gestionar alertas
class AlertManager {
    constructor() {
        this.alertsContainer = document.getElementById('alerts-container');
        this.alerts = [];
        this.maxAlerts = 5; // Máximo número de alertas visibles
        this.init();
    }

    init() {
        // Iniciar comprobación periódica de alertas
        this.checkAlerts();
        setInterval(() => this.checkAlerts(), 60000); // Cada minuto
    }

    async checkAlerts() {
        try {
            const response = await fetch('/api/alerts');
            const newAlerts = await response.json();
            
            // Verificar si hay nuevas alertas
            const currentAlertIds = this.alerts.map(a => a.id);
            const newAlertItems = newAlerts.filter(alert => 
                !currentAlertIds.includes(alert.id)
            );

            // Añadir nuevas alertas
            newAlertItems.forEach(alert => this.addAlert(alert));

            // Verificar alertas meteorológicas
            if (window.weatherManager) {
                const weatherAlerts = window.weatherManager.checkDangerousConditions();
                weatherAlerts.forEach(alert => this.addAlert({
                    ...alert,
                    id: `weather-${Date.now()}`,
                    source: 'weather'
                }));
            }

        } catch (error) {
            console.error('Error comprobando alertas:', error);
            this.addAlert({
                id: `error-${Date.now()}`,
                type: 'error',
                message: 'Error al comprobar alertas',
                severity: 'low'
            });
        }
    }

    addAlert(alert) {
        // Crear elemento de alerta
        const alertElement = this.createAlertElement(alert);
        
        // Añadir a la lista de alertas
        this.alerts.push({
            ...alert,
            element: alertElement
        });

        // Añadir al DOM
        this.alertsContainer.appendChild(alertElement);

        // Limitar número de alertas visibles
        this.limitAlerts();

        // Auto-eliminar después de un tiempo según severidad
        const timeout = this.getTimeoutBySeverity(alert.severity);
        setTimeout(() => this.removeAlert(alert.id), timeout);
    }

    createAlertElement(alert) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert ${alert.severity}`;
        alertDiv.setAttribute('data-alert-id', alert.id);

        // Crear contenido de la alerta
        alertDiv.innerHTML = `
            <div class="alert-content">
                <div class="alert-header">
                    ${this.getAlertIcon(alert.type)}
                    <span class="alert-title">${this.getAlertTitle(alert.type)}</span>
                    <button class="alert-close" onclick="window.alertManager.removeAlert('${alert.id}')">×</button>
                </div>
                <div class="alert-message">${alert.message}</div>
                ${alert.details ? `<div class="alert-details">${alert.details}</div>` : ''}
            </div>
        `;

        // Añadir animación de entrada
        alertDiv.style.animation = 'slideIn 0.3s ease-out';

        return alertDiv;
    }

    removeAlert(alertId) {
        const alertIndex = this.alerts.findIndex(a => a.id === alertId);
        if (alertIndex === -1) return;

        const alert = this.alerts[alertIndex];
        
        // Añadir animación de salida
        alert.element.style.animation = 'slideOut 0.3s ease-out';
        
        // Eliminar después de la animación
        setTimeout(() => {
            alert.element.remove();
            this.alerts.splice(alertIndex, 1);
        }, 300);
    }

    limitAlerts() {
        while (this.alerts.length > this.maxAlerts) {
            const oldestAlert = this.alerts[0];
            this.removeAlert(oldestAlert.id);
        }
    }

    getTimeoutBySeverity(severity) {
        const timeouts = {
            high: 0, // No auto-eliminar alertas graves
            medium: 300000, // 5 minutos
            low: 60000 // 1 minuto
        };
        return timeouts[severity] || timeouts.medium;
    }

    getAlertIcon(type) {
        const icons = {
            error: '⚠️',
            warning: '⚡',
            info: 'ℹ️',
            success: '✅',
            weather: '🌤️',
            wave: '🌊'
        };
        return icons[type] || icons.info;
    }

    getAlertTitle(type) {
        const titles = {
            error: 'Error',
            warning: 'Advertencia',
            info: 'Información',
            success: 'Éxito',
            weather: 'Alerta Meteorológica',
            wave: 'Alerta de Oleaje'
        };
        return titles[type] || 'Alerta';
    }
}

// Crear instancia global
window.alertManager = new AlertManager();

// Exportar para uso en otros módulos
export default AlertManager;
