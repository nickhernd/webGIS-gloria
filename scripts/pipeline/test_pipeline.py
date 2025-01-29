"""
Script de Prueba del Pipeline Completo

Este script ejecuta y verifica todo el flujo de procesamiento de datos,
desde la obtención hasta la visualización.

Autor: Jaime Hernández
Actualizado: 2025
"""

import sys
import os
from pathlib import Path
import logging
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Dict, Optional

load_dotenv()

# Añadir directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pipeline_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PipelineTester:
    def __init__(self):
        self.data_dir = ROOT_DIR / 'data'
        self._setup_environment()

    def _setup_environment(self) -> None:
        """Verifica y configura el entorno necesario."""
        try:
            # Verificar variables de entorno
            required_vars = ['COPERNICUS_USERNAME', 'COPERNICUS_PASSWORD', 'OPENWEATHER_API_KEY']
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            
            if missing_vars:
                raise EnvironmentError(f"Faltan variables de entorno: {', '.join(missing_vars)}")

            # Crear estructura de directorios
            directories = [
                self.data_dir / 'raw' / 'copernicus',
                self.data_dir / 'processed' / 'daily',
                self.data_dir / 'processed' / 'geographic',
                self.data_dir / 'processed' / 'weather',
                self.data_dir / 'temp',
                ROOT_DIR / 'logs'
            ]

            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)

        except Exception as e:
            logger.error(f"Error en configuración: {str(e)}")
            raise

    async def run_pipeline(self) -> bool:
        """Ejecuta el pipeline completo."""
        try:
            logger.info("Iniciando pipeline de prueba...")

            # 1. Obtener datos de Copernicus
            logger.info("Paso 1: Obteniendo datos de Copernicus")
            from backend.core.obtain_data import CopernicusDataRetriever
            retriever = CopernicusDataRetriever()
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            region = {
                'minlon': -5.5,
                'maxlon': 36.0,
                'minlat': 30.0,
                'maxlat': 46.0
            }
            
            wave_data = retriever.get_wave_data(start_date, end_date, region)
            if wave_data is None:
                raise Exception("Fallo en obtención de datos Copernicus")

            # 2. Convertir datos NC a CSV
            logger.info("Paso 2: Convirtiendo datos NC a CSV")
            from backend.data_processing.nc_to_csv import NetCDFConverter
            converter = NetCDFConverter()
            if not converter.convert_file('wave_data.nc', 'wave'):
                raise Exception("Fallo en conversión NC a CSV")

            # 3. Procesar datos geográficos
            logger.info("Paso 3: Procesando datos geográficos")
            from backend.data_processing.csv_to_json import GeoJSONConverter
            geo_converter = GeoJSONConverter()
            if not geo_converter.convert_to_geojson('wave_data.csv', 'wave_data.geojson'):
                raise Exception("Fallo en conversión a GeoJSON")

            # 4. Obtener datos meteorológicos
            logger.info("Paso 4: Obteniendo datos meteorológicos")
            from backend.core.openweather_data import OpenWeatherAPI
            weather_api = OpenWeatherAPI()
            
            locations = [
                {'lat': 38.5, 'lon': -0.5},
                {'lat': 39.0, 'lon': -0.3}
            ]
            
            weather_data = await weather_api.process_locations(locations)
            if not weather_data:
                raise Exception("Fallo en obtención de datos meteorológicos")

            # 5. Procesar anomalías
            logger.info("Paso 5: Procesando anomalías")
            from backend.data_processing.anomalies_to_json import AnomalyDetector
            detector = AnomalyDetector()
            
            if not detector.process_file('wave_data.csv', 'anomalies.geojson'):
                raise Exception("Fallo en detección de anomalías")

            # 6. Insertar datos de lonja
            logger.info("Paso 6: Insertando datos de lonja")
            from backend.data_processing.insert_lonja_and_img import LonjaProcessor
            lonja_processor = LonjaProcessor()
            
            if not lonja_processor.process_file('recintos.geojson', 'lonjas.csv'):
                raise Exception("Fallo en inserción de datos de lonja")

            logger.info("Pipeline completado exitosamente")
            return True

        except Exception as e:
            logger.error(f"Error en pipeline: {str(e)}")
            return False

async def main():
    tester = PipelineTester()
    success = await tester.run_pipeline()
    
    if success:
        logger.info("Test del pipeline completado exitosamente")
        sys.exit(0)
    else:
        logger.error("Test del pipeline fallido")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
