// Inicialización del mapa
let map;
let markers = [];
let currentGeoJSON = null;

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar el mapa centrado en España
    map = L.map('map').setView([40.4168, -3.7038], 6);

    // Añadir capa de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Cargar datos de piscifactorías
    loadFarmData();
});

// Función para cargar datos de piscifactorías
async function loadFarmData() {
    try {
        const response = await fetch('/api/farms/geojson');
        const geojsonData = await response.json();
        
        // Limpiar marcadores existentes
        clearMarkers();
        
        // Guardar referencia a los datos actuales
        currentGeoJSON = geojsonData;
        
        // Añadir nueva capa GeoJSON
        L.geoJSON(geojsonData, {
            pointToLayer: createCustomMarker,
            onEachFeature: bindPopupToFeature
        }).addTo(map);
        
        // Ajustar vista a los datos
        fitMapToBounds();
        
    } catch (error) {
        console.error('Error cargando datos de piscifactorías:', error);
        showAlert('Error cargando datos del mapa', 'error');
    }
}

// Función para crear marcadores personalizados
function createCustomMarker(feature, latlng) {
    const marker = L.circleMarker(latlng, {
        radius: 8,
        fillColor: getMarkerColor(feature.properties.status),
        color: "#fff",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    });
    
    markers.push(marker);
    return marker;
}

// Función para determinar el color del marcador según el estado
function getMarkerColor(status) {
    const colors = {
        normal: "#4ade80",    // Verde para estado normal
        warning: "#fbbf24",   // Amarillo para alertas
        danger: "#ef4444",    // Rojo para peligro
        inactive: "#9ca3af"   // Gris para inactivo
    };
    return colors[status] || colors.normal;
}

// Función para vincular popups a los marcadores
function bindPopupToFeature(feature, layer) {
    // Crear contenido del popup
    const popupContent = createPopupContent(feature.properties);
    
    // Vincular popup y eventos
    layer.bindPopup(popupContent);
    
    layer.on({
        click: (e) => {
            showInfoPanel(feature.properties);
            updateCharts(feature.properties.id);
        },
        mouseover: (e) => {
            const layer = e.target;
            layer.setStyle({
                fillOpacity: 1
            });
        },
        mouseout: (e) => {
            const layer = e.target;
            layer.setStyle({
                fillOpacity: 0.8
            });
        }
    });
}

// Función para crear el contenido del popup
function createPopupContent(properties) {
    return `
        <div class="popup-content">
            <h3>${properties.name}</h3>
            <p>Estado: ${properties.status}</p>
            <p>Última actualización: ${properties.lastUpdate}</p>
        </div>
    `;
}

// Función para mostrar el panel de información
function showInfoPanel(properties) {
    const panel = document.getElementById('info-panel');
    const content = document.querySelector('.panel-content');
    
    content.innerHTML = `
        <h3>${properties.name}</h3>
        <div class="info-group">
            <label>Estado:</label>
            <span class="status-${properties.status}">${properties.status}</span>
        </div>
        <div class="info-group">
            <label>Ubicación:</label>
            <span>${properties.coordinates.join(', ')}</span>
        </div>
        <div class="info-group">
            <label>Última actualización:</label>
            <span>${properties.lastUpdate}</span>
        </div>
        <div class="charts-container">
            <canvas id="farmChart"></canvas>
        </div>
    `;
    
    panel.classList.add('active');
}

// Función para limpiar marcadores
function clearMarkers() {
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
}

// Función para ajustar la vista del mapa
function fitMapToBounds() {
    if (currentGeoJSON && currentGeoJSON.features.length > 0) {
        const bounds = L.geoJSON(currentGeoJSON).getBounds();
        map.fitBounds(bounds, { padding: [50, 50] });
    }
}

// Escuchar evento para cerrar panel de información
document.getElementById('close-panel').addEventListener('click', function() {
    document.getElementById('info-panel').classList.remove('active');
});

// Función para mostrar alertas en el mapa
function showAlert(message, type = 'info') {
    const alertsContainer = document.getElementById('alerts-container');
    const alert = document.createElement('div');
    alert.className = `alert ${type}`;
    alert.textContent = message;
    
    alertsContainer.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}

// Exportar funciones necesarias
window.mapManager = {
    loadFarmData,
    showAlert,
    updateMarkerStatus: function(farmId, status) {
        // Actualizar estado de marcador específico
        if (currentGeoJSON) {
            const feature = currentGeoJSON.features.find(f => f.properties.id === farmId);
            if (feature) {
                feature.properties.status = status;
                loadFarmData(); // Recargar mapa
            }
        }
    }
};
