#!/bin/bash

# Colores para los mensajes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Función para mostrar mensajes
log_message() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Verificar que estamos en el entorno virtual correcto
if [[ "$VIRTUAL_ENV" != *"gloria-env"* ]]; then
    log_message "${RED}Error: Entorno virtual incorrecto${NC}"
    log_message "Por favor, ejecuta: source ~/virtualenvs/gloria-env/bin/activate"
    exit 1
fi

# Verificar que existe .env
if [ ! -f .env ] || ! grep -q "COPERNICUS_USERNAME" .env; then
    log_message "${RED}No se encontraron credenciales de Copernicus${NC}"
    log_message "Configurando credenciales..."
    python setup_copernicus.py
fi

# Crear directorios necesarios
mkdir -p data/{raw,processed}/{copernicus,geographic,weather,analysis}
mkdir -p data/processed/daily/data_by_date
mkdir -p logs

# Iniciar el backend
log_message "${GREEN}Iniciando backend...${NC}"
uvicorn backend.api.main:app --reload --port 8000 &
BACKEND_PID=$!

# Esperar a que el backend esté listo
sleep 5

# Ejecutar el pipeline
log_message "${GREEN}Ejecutando pipeline de datos...${NC}"
python scripts/pipeline/test_pipeline.py &
PIPELINE_PID=$!

# Iniciar el servidor frontend
log_message "${GREEN}Iniciando servidor frontend...${NC}"
cd public
python -m http.server 8001 &
FRONTEND_PID=$!

# Volver al directorio raíz
cd ..

log_message "${GREEN}Sistema iniciado correctamente${NC}"
log_message "Backend corriendo en: http://localhost:8000"
log_message "Frontend corriendo en: http://localhost:8001"
log_message "Documentación API en: http://localhost:8000/docs"

# Función para limpiar procesos al salir
cleanup() {
    log_message "${RED}Deteniendo servicios...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $PIPELINE_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    log_message "${GREEN}Sistema detenido correctamente${NC}"
    exit 0
}

# Capturar señal de interrupción
trap cleanup SIGINT

# Mantener el script corriendo y mostrar logs
tail -f logs/pipeline.log
