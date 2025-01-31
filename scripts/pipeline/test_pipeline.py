"""
Pipeline Principal de Procesamiento de Datos

Este script gestiona el pipeline completo de obtención, procesamiento y 
análisis de datos para el sistema de monitoreo de piscifactorías.

Autor: Sebastian Pasker
Actualizado: 2024
"""

import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List
from dotenv import load_dotenv

# Configuración inicial
load_dotenv()
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataPipeline:
    def __init__(self):
        self.root_dir = ROOT_DIR
        self.data_dir = self.root_dir / 'data'
        self.config = self._cargar_config()
        self._configurar_entorno()
        
    def _cargar_config(self) -> Dict:
        """Carga la configuración desde variables de entorno."""
        return {
            'copernicus': {
                'username': os.getenv('COPERNICUS_USERNAME'),
                'password': os.getenv('COPERNICUS_PASSWORD')
            },
            'openweather': {
                'api_key': os.getenv('OPENWEATHER_API_KEY')
            },
            'coordinates': {
                'minlon': -5.5,
                'maxlon': 36.0,
                'minlat': 30.1875,
                'maxlat': 45.97916793823242
            },
            'time_range': {
                'days': 7
            }
        }

    def _configurar_entorno(self) -> None:
        """Configura los directorios necesarios y verifica la configuración."""
        try:
            # Verificar variables de entorno
            configuraciones_requeridas = [
                ('copernicus', ['username', 'password']),
                ('openweather', ['api_key'])
            ]
            
            for servicio, claves in configuraciones_requeridas:
                for clave in claves:
                    if not self.config[servicio][clave]:
                        raise EnvironmentError(
                            f"Falta configuración: {servicio}.{clave}"
                        )

            # Crear estructura de directorios
            directorios = [
                self.data_dir / 'raw' / 'copernicus',
                self.data_dir / 'raw' / 'geographic',
                self.data_dir / 'processed' / 'daily',
                self.data_dir / 'processed' / 'geographic',
                self.data_dir / 'processed' / 'weather',
                self.data_dir / 'processed' / 'analysis',
                self.data_dir / 'temp',
                self.root_dir / 'logs'
            ]

            for directorio in directorios:
                directorio.mkdir(parents=True, exist_ok=True)

        except Exception as e:
            logger.error(f"Error en la configuración: {str(e)}")
            raise

    def _obtener_coordenadas_piscifactorias(self) -> List[Dict[str, float]]:
        """Obtiene las coordenadas de las piscifactorías desde los datos geográficos."""
        try:
            import json
            from backend.data_processing.calculate_center import calculate_centers
            
            archivo_geojson = self.data_dir / 'raw/geographic/recintos_buffer.geojson'
            with open(archivo_geojson) as f:
                datos = json.load(f)
            
            # Calcular centros de cada piscifactoría
            centros = calculate_centers(datos)
            return centros
            
        except Exception as e:
            logger.error(f"Error al obtener coordenadas de piscifactorías: {str(e)}")
            return []

    def _obtener_datos_copernicus(self) -> bool:
        """Obtiene datos de Copernicus Marine."""
        try:
            from backend.core.obtain_data import CopernicusDataRetriever
            
            logger.info("Iniciando obtención de datos Copernicus...")
            recuperador = CopernicusDataRetriever()
            
            # Configurar credenciales
            recuperador.username = self.config['copernicus']['username']
            recuperador.password = self.config['copernicus']['password']
            
            fecha_fin = datetime.now()
            fecha_inicio = fecha_fin - timedelta(
                days=self.config['time_range']['days']
            )
            
            # Obtener datos de oleaje
            datos_oleaje = recuperador.get_wave_data(
                fecha_inicio, 
                fecha_fin, 
                self.config['coordinates']
            )
            if datos_oleaje is None:
                raise Exception("Error al obtener datos de oleaje")
                
            # Guardar datos de oleaje
            archivo_oleaje = self.data_dir / 'raw/copernicus/wave_data.nc'
            if not recuperador.save_dataset(datos_oleaje, str(archivo_oleaje), 'wave'):
                raise Exception("Error al guardar datos de oleaje")
                
            logger.info("Datos Copernicus obtenidos exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en obtención de datos Copernicus: {str(e)}")
            return False

    async def _obtener_datos_meteorologicos(self) -> bool:
        """Obtiene datos meteorológicos para cada ubicación de piscifactoría."""
        try:
            from backend.core.openweather_data import OpenWeatherAPI
            
            logger.info("Iniciando obtención de datos meteorológicos...")
            api_meteorologica = OpenWeatherAPI(
                api_key=self.config['openweather']['api_key']
            )
            
            # Obtener coordenadas de piscifactorías
            coordenadas = self._obtener_coordenadas_piscifactorias()
            if not coordenadas:
                raise Exception("No se encontraron coordenadas de piscifactorías")
            
            # Obtener datos meteorológicos
            datos_meteorologicos = await api_meteorologica.process_locations(coordenadas)
            if not datos_meteorologicos:
                raise Exception("Error al obtener datos meteorológicos")
                
            # Guardar datos
            archivo_meteorologico = self.data_dir / 'processed/weather/weather_data.json'
            if not await api_meteorologica.save_weather_data(datos_meteorologicos, str(archivo_meteorologico)):
                raise Exception("Error al guardar datos meteorológicos")
                
            logger.info("Datos meteorológicos obtenidos exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en obtención de datos meteorológicos: {str(e)}")
            return False

    def _procesar_datos_geograficos(self) -> bool:
        """Procesa datos geográficos y calcula centros."""
        try:
            from backend.data_processing.calculate_center import process_geographic_data
            
            logger.info("Iniciando procesamiento de datos geográficos...")
            
            archivo_entrada = self.data_dir / 'raw/geographic/recintos_buffer.geojson'
            archivo_salida = self.data_dir / 'processed/geographic/recintos_with_data_center.geojson'
            
            if not process_geographic_data(str(archivo_entrada), str(archivo_salida)):
                raise Exception("Error al procesar datos geográficos")
                
            logger.info("Datos geográficos procesados exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en procesamiento de datos geográficos: {str(e)}")
            return False

    def _procesar_datos_netcdf(self) -> bool:
        """Procesa datos NetCDF a formato CSV."""
        try:
            from backend.data_processing.nc_to_csv import NetCDFConverter
            
            logger.info("Iniciando conversión de datos NetCDF...")
            convertidor = NetCDFConverter()
            
            # Convertir datos de oleaje
            entrada_oleaje = self.data_dir / 'raw/copernicus/wave_data.nc'
            salida_oleaje = self.data_dir / 'temp/wave_data.csv'
            
            if not convertidor.convert_file(str(entrada_oleaje), str(salida_oleaje)):
                raise Exception("Error al convertir datos de oleaje")
                
            logger.info("Conversión de datos NetCDF completada")
            return True
            
        except Exception as e:
            logger.error(f"Error en procesamiento de datos NetCDF: {str(e)}")
            return False

    def _generar_datos_diarios(self) -> bool:
        """Genera archivos de datos diarios a partir de datos procesados."""
        try:
            from backend.data_processing.separate_by_date import separate_data_by_date
            
            logger.info("Iniciando generación de datos diarios...")
            
            archivo_entrada = self.data_dir / 'temp/wave_data.csv'
            directorio_salida = self.data_dir / 'processed/daily/data_by_date'
            
            if not separate_data_by_date(str(archivo_entrada), str(directorio_salida)):
                raise Exception("Error al generar datos diarios")
                
            logger.info("Datos diarios generados exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en generación de datos diarios: {str(e)}")
            return False

    def _generar_analisis(self) -> bool:
        """Genera datos de análisis y coropletas."""
        try:
            from backend.data_processing.csv_to_json import convert_to_geojson
            from scripts.create_choropleth import create_choropleth
            
            logger.info("Iniciando generación de datos de análisis...")
            
            # Convertir datos procesados a GeoJSON
            csv_entrada = self.data_dir / 'temp/wave_data.csv'
            geojson_salida = self.data_dir / 'processed/analysis/data_choropleth.geojson'
            
            if not convert_to_geojson(str(csv_entrada), str(geojson_salida)):
                raise Exception("Error al convertir datos a GeoJSON")
                
            # Crear visualización de coropletas
            if not create_choropleth(str(geojson_salida)):
                raise Exception("Error al crear coropletas")
                
            logger.info("Datos de análisis generados exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en generación de análisis: {str(e)}")
            return False

    async def ejecutar(self) -> bool:
        """Ejecuta el pipeline completo de datos."""
        try:
            logger.info("Iniciando ejecución del pipeline de datos...")
            
            # Paso 1: Obtener datos Copernicus
            if not self._obtener_datos_copernicus():
                raise Exception("Falló la obtención de datos Copernicus")
            
            # Paso 2: Obtener datos meteorológicos
            if not await self._obtener_datos_meteorologicos():
                raise Exception("Falló la obtención de datos meteorológicos")
            
            # Paso 3: Procesar datos geográficos
            if not self._procesar_datos_geograficos():
                raise Exception("Falló el procesamiento de datos geográficos")
            
            # Paso 4: Procesar datos NetCDF
            if not self._procesar_datos_netcdf():
                raise Exception("Falló el procesamiento de datos NetCDF")
            
            # Paso 5: Generar datos diarios
            if not self._generar_datos_diarios():
                raise Exception("Falló la generación de datos diarios")
            
            # Paso 6: Generar análisis
            if not self._generar_analisis():
                raise Exception("Falló la generación de análisis")
            
            logger.info("Pipeline de datos completado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en la ejecución del pipeline: {str(e)}")
            return False

if __name__ == "__main__":
    # Configurar y ejecutar el pipeline
    pipeline = DataPipeline()
    asyncio.run(pipeline.ejecutar())
