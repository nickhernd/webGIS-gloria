// Estado global de la aplicación
const appState = {
    selectedFarm: null,
    isLoading: false,
    lastUpdate: null
};

// Función principal de inicialización
document.addEventListener('DOMContentLoaded', function() {
    initializeApplication();
});

async function initializeApplication() {
    try {
        appState.isLoading = true;
        updateLoadingState();

        // Inicializar todas las partes de la aplicación
        await Promise.all([
            initializeMap(),
            initializeCharts(),
            checkPipelineStatus()
        ]);

        // Configurar actualizaciones periódicas
        setupPeriodicUpdates();

        appState.isLoading = false;
        updateLoadingState();
        
        // Mostrar mensaje de éxito
        window.alertManager?.addAlert({
            id: `init-${Date.now()}`,
            type: 'success',
            message: 'Sistema inicializado correctamente',
            severity: 'low'
        });

    } catch (error) {
        console.error('Error inicializando la aplicación:', error);
        appState.isLoading = false;
        updateLoadingState();
        
        window.alertManager?.addAlert({
            id: `error-${Date.now()}`,
            type: 'error',
            message: 'Error inicializando el sistema',
            severity: 'high'
        });
    }
}

// Inicialización del mapa
async function initializeMap() {
    if (!window.mapManager) {
        throw new Error('Map Manager no inicializado');
    }
    await window.mapManager.loadFarmData();
}

// Inicialización de gráficos
async function initializeCharts() {
    if (!window.chartManager) {
        throw new Error('Chart Manager no inicializado');
    }
    await window.chartManager.updateWaveChart();
}

// Comprobar estado del pipeline
async function checkPipelineStatus() {
    try {
        const response = await fetch('/api/pipeline/status');
        const status = await response.json();
        
        updatePipelineStatus(status);
        
    } catch (error) {
        console.error('Error comprobando estado del pipeline:', error);
        throw error;
    }
}

// Actualizar estado del pipeline en la UI
function updatePipelineStatus(status) {
    const statusElement = document.getElementById('pipeline-status');
    if (!statusElement) return;

    statusElement.className = `status-indicator ${status.running ? 'active' : ''}`;
    statusElement.textContent = status.running ? 'En ejecución' : 'Detenido';
}

// Configurar actualizaciones periódicas
function setupPeriodicUpdates() {
    // Actualizar datos cada 5 minutos
    setInterval(async () => {
        try {
            await updateAllData();
            appState.lastUpdate = new Date();
            
        } catch (error) {
            console.error('Error en actualización periódica:', error);
            window.alertManager?.addAlert({
                id: `update-error-${Date.now()}`,
                type: 'error',
                message: 'Error actualizando datos',
                severity: 'medium'
            });
        }
    }, 300000);

    // Comprobar estado del pipeline cada minuto
    setInterval(checkPipelineStatus, 60000);
}

// Actualizar todos los datos
async function updateAllData() {
    appState.isLoading = true;
    updateLoadingState();

    try {
        await Promise.all([
            window.mapManager?.loadFarmData(),
            window.chartManager?.updateWaveChart(),
            window.weatherManager?.updateWeather()
        ]);

        if (appState.selectedFarm) {
            await window.chartManager?.updateFarmChart(appState.selectedFarm);
        }

    } catch (error) {
        console.error('Error actualizando datos:', error);
        throw error;
    } finally {
        appState.isLoading = false;
        updateLoadingState();
    }
}

// Actualizar estado de carga en la UI
function updateLoadingState() {
    const loadingIndicator = document.querySelector('.loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = appState.isLoading ? 'block' : 'none';
    }
}

// Manejar selección de piscifactoría
function handleFarmSelection(farmId) {
    appState.selectedFarm = farmId;
    window.chartManager?.updateFarmChart(farmId);
}

// Exportar funciones necesarias
window.appManager = {
    updateAllData,
    handleFarmSelection,
    getState: () => appState
};
