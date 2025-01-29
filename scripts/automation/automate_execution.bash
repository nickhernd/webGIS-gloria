#!/bin/bash

"""
Script de Automatización de Ejecución

Este script automatiza la ejecución del pipeline completo de procesamiento de datos.
Gestiona la obtención, transformación y análisis de datos oceanográficos y meteorológicos.

Autor: Jaime Hernández
Actualizado: 2025
"""

# Configuración de logging
LOG_FILE="logs/automation.log"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATA_DIR="${SCRIPT_DIR}/../data"

# Función para logging
log() {
    local message=$1
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "${timestamp} - ${message}" >> "${LOG_FILE}"
    echo "${timestamp} - ${message}"
}

# Verificar directorios necesarios
check_directories() {
    log "Verificando directorios necesarios..."
    
    directories=(
        "${DATA_DIR}/raw/copernicus"
        "${DATA_DIR}/processed"
        "${DATA_DIR}/temp"
        "logs"
    )

    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            log "Creando directorio: $dir"
            mkdir -p "$dir"
        fi
    done
}

# Verificar variables de entorno
check_environment() {
    log "Verificando variables de entorno..."
    
    if [ -z "$COPERNICUS_USERNAME" ] || [ -z "$COPERNICUS_PASSWORD" ]; then
        log "ERROR: Variables de entorno de Copernicus no configuradas"
        exit 1
    fi

    if [ -z "$OPENWEATHER_API_KEY" ]; then
        log "ERROR: API KEY de OpenWeather no configurada"
        exit 1
    }
}

# Ejecutar pipeline de procesamiento
execute_pipeline() {
    log "Iniciando ejecución del pipeline..."

    # 1. Obtener datos de Copernicus
    log "Obteniendo datos de Copernicus..."
    if ! python3 "${SCRIPT_DIR}/obtain_data.py"; then
        log "ERROR: Fallo en obtain_data.py"
        return 1
    fi

    # 2. Convertir NC a CSV
    log "Convirtiendo datos NC a CSV..."
    if ! python3 "${SCRIPT_DIR}/nc_to_csv.py"; then
        log "ERROR: Fallo en nc_to_csv.py"
        return 1
    fi

    # 3. Procesar datos
    log "Procesando datos..."
    if ! python3 "${SCRIPT_DIR}/csv_to_json.py"; then
        log "ERROR: Fallo en csv_to_json.py"
        return 1
    fi

    # 4. Obtener datos meteorológicos
    log "Obteniendo datos meteorológicos..."
    if ! python3 "${SCRIPT_DIR}/data_with_openweather.py"; then
        log "ERROR: Fallo en data_with_openweather.py"
        return 1
    fi

    # 5. Procesar y ordenar datos
    log "Ordenando datos por punto..."
    if ! python3 "${SCRIPT_DIR}/order_csv_by_point.py"; then
        log "ERROR: Fallo en order_csv_by_point.py"
        return 1
    fi

    # 6. Calcular centroides
    log "Calculando centroides..."
    if ! python3 "${SCRIPT_DIR}/calculate_center.py"; then
        log "ERROR: Fallo en calculate_center.py"
        return 1
    fi

    # 7. Detectar anomalías
    log "Detectando anomalías..."
    if ! python3 "${SCRIPT_DIR}/anomalies_to_json.py"; then
        log "ERROR: Fallo en anomalies_to_json.py"
        return 1
    fi

    # 8. Separar por fecha
    log "Separando datos por fecha..."
    if ! python3 "${SCRIPT_DIR}/separate_by_date.py"; then
        log "ERROR: Fallo en separate_by_date.py"
        return 1
    fi

    log "Pipeline completado exitosamente"
    return 0
}

# Limpiar archivos temporales
cleanup() {
    log "Limpiando archivos temporales..."
    rm -f "${DATA_DIR}/temp"/*
}

# Función principal
main() {
    log "Iniciando proceso de automatización..."
    
    check_directories
    check_environment
    
    if execute_pipeline; then
        cleanup
        log "Proceso completado exitosamente"
        return 0
    else
        log "ERROR: Proceso fallido"
        return 1
    fi
}

# Ejecutar script
main "$@"
