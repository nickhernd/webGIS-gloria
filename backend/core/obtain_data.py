#!/usr/bin/env python3
"""
Módulo de Obtención de Datos de Copernicus Marine

Este módulo gestiona la obtención de datos de oleaje y bioquímicos del servicio Copernicus Marine.
Utiliza la librería Python de Copernicus Marine para descargar datos de parámetros específicos y
áreas geográficas.

Autor: Jaime Hernández
Actualizado: Enero 2025
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any
import logging
from pathlib import Path

import copernicusmarine
import xarray as xr
import numpy as np

# Configuración del logging
logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   handlers=[
       logging.FileHandler('logs/copernicus_data.log'),
       logging.StreamHandler()
   ]
)
logger = logging.getLogger(__name__)

class CopernicusDataRetriever:
   """Gestiona la obtención de datos del servicio Copernicus Marine."""
   
   def __init__(self, config_path: Optional[str] = None):
       """
       Inicializa el obtendor de datos con configuración opcional.
       
       Args:
           config_path: Ruta al archivo de configuración (opcional)
       """
       self.config = self._load_config(config_path) if config_path else {}
       self._validate_environment()
       
   def _validate_environment(self) -> None:
       """Valida que las variables de entorno requeridas estén configuradas."""
       if not os.getenv('COPERNICUS_USERNAME') or not os.getenv('COPERNICUS_PASSWORD'):
           raise EnvironmentError(
               "No se encontraron las credenciales de Copernicus en las variables de entorno. "
               "Por favor, configure COPERNICUS_USERNAME y COPERNICUS_PASSWORD"
           )
   
   def get_wave_data(
       self,
       start_date: datetime,
       end_date: datetime,
       region: Dict[str, float]
   ) -> Optional[xr.Dataset]:
       """
       Obtiene datos de oleaje de Copernicus Marine.
       
       Args:
           start_date: Fecha de inicio para la obtención de datos
           end_date: Fecha de fin para la obtención de datos
           region: Diccionario con coordenadas bbox {minlon, maxlon, minlat, maxlat}
       
       Returns:
           Dataset de xarray conteniendo datos de oleaje o None si la obtención falla
       """
       try:
           logger.info(f"Obteniendo datos de oleaje desde {start_date} hasta {end_date}")
           
           dataset_id = "cmems_mod_med_wav_anfc_4.2km_PT1H-i"
           variables = ["VHM0", "VMDR", "VPED"]
           
           data = copernicusmarine.open_dataset(
               dataset_id=dataset_id,
               variables=variables,
               minimum_longitude=region['minlon'],
               maximum_longitude=region['maxlon'],
               minimum_latitude=region['minlat'],
               maximum_latitude=region['maxlat'],
               start_datetime=start_date.strftime('%Y-%m-%d %H:%M:%S'),
               end_datetime=end_date.strftime('%Y-%m-%d %H:%M:%S')
           )
           
           logger.info("Datos de oleaje obtenidos con éxito")
           return data
           
       except Exception as e:
           logger.error(f"Error al obtener datos de oleaje: {str(e)}")
           return None
   
   def get_biogeochemistry_data(
       self,
       start_date: datetime,
       end_date: datetime,
       region: Dict[str, float]
   ) -> Optional[xr.Dataset]:
       """
       Obtiene datos bioquímicos de Copernicus Marine.
       
       Args:
           start_date: Fecha de inicio para la obtención de datos
           end_date: Fecha de fin para la obtención de datos
           region: Diccionario con coordenadas bbox {minlon, maxlon, minlat, maxlat}
       
       Returns:
           Dataset de xarray conteniendo datos bioquímicos o None si la obtención falla
       """
       try:
           logger.info(f"Obteniendo datos bioquímicos desde {start_date} hasta {end_date}")
           
           dataset_id = "cmems_mod_med_bgc-bio_anfc_4.2km_P1D-m"
           variables = ["o2", "pH"]
           
           data = copernicusmarine.open_dataset(
               dataset_id=dataset_id,
               variables=variables,
               minimum_longitude=region['minlon'],
               maximum_longitude=region['maxlon'],
               minimum_latitude=region['minlat'],
               maximum_latitude=region['maxlat'],
               start_datetime=start_date.strftime('%Y-%m-%d %H:%M:%S'),
               end_datetime=end_date.strftime('%Y-%m-%d %H:%M:%S')
           )
           
           logger.info("Datos bioquímicos obtenidos con éxito")
           return data
           
       except Exception as e:
           logger.error(f"Error al obtener datos bioquímicos: {str(e)}")
           return None
   
   def save_dataset(
    self,
    dataset: xr.Dataset,
    output_path: str,
    dataset_type: str
) -> bool:
    """
    Guarda un dataset en archivo NetCDF.
    
    Args:
        dataset: Dataset de xarray para guardar
        output_path: Ruta donde guardar el archivo
        dataset_type: Tipo de dataset ('wave' o 'bio')
    
    Returns:
        bool indicando éxito o fracaso
    """
    try:
        # Convertir a ruta absoluta
        root_dir = Path(__file__).parent.parent.parent
        full_path = root_dir / output_path
        
        # Crear directorio si no existe
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar dataset
        dataset.to_netcdf(str(full_path))
        logger.info(f"Dataset guardado con éxito en {full_path}")
        return True
    except Exception as e:
        logger.error(f"Error al guardar dataset: {str(e)}")
        return False

def main():
    """Función principal de ejecución."""
    try:
        retriever = CopernicusDataRetriever()
        
        # Definir rango de tiempo y región
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        region = {
            'minlon': -5.5,
            'maxlon': 36.0,
            'minlat': 30.0,
            'maxlat': 46.0
        }
        
        # Verificar y crear directorios necesarios
        root_dir = Path(__file__).parent.parent.parent
        data_dir = root_dir / 'data'
        copernicus_dir = data_dir / 'raw' / 'copernicus'
        copernicus_dir.mkdir(parents=True, exist_ok=True)
        
        # Obtener y guardar datos de oleaje
        logger.info("Iniciando obtención de datos de oleaje...")
        wave_data = retriever.get_wave_data(start_date, end_date, region)
        if wave_data is not None:
            wave_path = 'data/raw/copernicus/wave_data.nc'
            if retriever.save_dataset(wave_data, wave_path, 'wave'):
                logger.info("Datos de oleaje guardados correctamente")
            else:
                logger.error("Error al guardar datos de oleaje")
        
        # Obtener y guardar datos bioquímicos
        logger.info("Iniciando obtención de datos bioquímicos...")
        bio_data = retriever.get_biogeochemistry_data(start_date, end_date, region)
        if bio_data is not None:
            bio_path = 'data/raw/copernicus/bio_data.nc'
            if retriever.save_dataset(bio_data, bio_path, 'bio'):
                logger.info("Datos bioquímicos guardados correctamente")
            else:
                logger.error("Error al guardar datos bioquímicos")

    except Exception as e:
        logger.error(f"Error en la ejecución principal: {str(e)}")
        return False
    
    return True
            
if __name__ == "__main__":
   main()
