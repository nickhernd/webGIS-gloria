#!/usr/bin/env python3
"""
Módulo de Conversión de NetCDF a CSV

Este módulo se encarga de convertir archivos NetCDF de Copernicus Marine a formato CSV.
Procesa los datos de oleaje y bioquímicos, aplicando las transformaciones necesarias
para su posterior análisis.
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

import xarray as xr
import pandas as pd
import numpy as np

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/data_conversion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NetCDFConverter:
    """Gestiona la conversión de archivos NetCDF a CSV."""

    def __init__(self, input_dir: str = 'data/raw/copernicus', output_dir: str = 'data/temp'):
        """
        Inicializa el convertidor de NetCDF.

        Args:
            input_dir: Directorio donde se encuentran los archivos NetCDF
            output_dir: Directorio donde se guardarán los archivos CSV
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self._create_directories()

    def _create_directories(self) -> None:
        """Crea los directorios necesarios si no existen."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_netcdf(self, file_path: Path) -> Optional[xr.Dataset]:
        """
        Carga un archivo NetCDF.

        Args:
            file_path: Ruta al archivo NetCDF

        Returns:
            Dataset de xarray o None si la carga falla
        """
        try:
            logger.info(f"Cargando archivo NetCDF: {file_path}")
            return xr.open_dataset(file_path)
        except Exception as e:
            logger.error(f"Error al cargar archivo NetCDF {file_path}: {str(e)}")
            return None

    def _process_wave_data(self, dataset: xr.Dataset) -> pd.DataFrame:
        """
        Procesa datos de oleaje del dataset.

        Args:
            dataset: Dataset de xarray con datos de oleaje

        Returns:
            DataFrame de pandas con los datos procesados
        """
        logger.info("Procesando datos de oleaje")
        try:
            # Extraer variables relevantes
            df = pd.DataFrame({
                'longitude': dataset.longitude.values.flatten(),
                'latitude': dataset.latitude.values.flatten(),
                'time': dataset.time.values.flatten(),
                'VHM0': dataset.VHM0.values.flatten(),  # Altura significativa de ola
                'VMDR': dataset.VMDR.values.flatten(),  # Dirección media
                'VPED': dataset.VPED.values.flatten()   # Período
            })

            # Limpiar datos
            df = df.dropna()
            
            # Convertir tiempo a formato datetime
            df['time'] = pd.to_datetime(df['time'])
            
            return df

        except Exception as e:
            logger.error(f"Error en el procesamiento de datos de oleaje: {str(e)}")
            raise

    def _process_bio_data(self, dataset: xr.Dataset) -> pd.DataFrame:
        """
        Procesa datos bioquímicos del dataset.

        Args:
            dataset: Dataset de xarray con datos bioquímicos

        Returns:
            DataFrame de pandas con los datos procesados
        """
        logger.info("Procesando datos bioquímicos")
        try:
            # Extraer variables relevantes
            df = pd.DataFrame({
                'longitude': dataset.longitude.values.flatten(),
                'latitude': dataset.latitude.values.flatten(),
                'time': dataset.time.values.flatten(),
                'o2': dataset.o2.values.flatten(),  # Oxígeno
                'pH': dataset.pH.values.flatten()   # pH
            })

            # Limpiar datos
            df = df.dropna()
            
            # Convertir tiempo a formato datetime
            df['time'] = pd.to_datetime(df['time'])
            
            return df

        except Exception as e:
            logger.error(f"Error en el procesamiento de datos bioquímicos: {str(e)}")
            raise

    def convert_file(self, input_file: str, data_type: str) -> bool:
        """
        Convierte un archivo NetCDF a CSV.

        Args:
            input_file: Nombre del archivo NetCDF a convertir
            data_type: Tipo de datos ('wave' o 'bio')

        Returns:
            bool indicando éxito o fracaso
        """
        try:
            input_path = self.input_dir / input_file
            dataset = self._load_netcdf(input_path)
            
            if dataset is None:
                return False

            # Procesar datos según el tipo
            if data_type == 'wave':
                df = self._process_wave_data(dataset)
                output_file = 'wave_data.csv'
            elif data_type == 'bio':
                df = self._process_bio_data(dataset)
                output_file = 'bio_data.csv'
            else:
                logger.error(f"Tipo de datos no reconocido: {data_type}")
                return False

            # Guardar a CSV
            output_path = self.output_dir / output_file
            df.to_csv(output_path, index=False)
            logger.info(f"Archivo convertido exitosamente: {output_path}")
            
            return True

        except Exception as e:
            logger.error(f"Error en la conversión del archivo: {str(e)}")
            return False

def main():
    """Función principal de ejecución."""
    converter = NetCDFConverter()
    
    # Convertir datos de oleaje
    converter.convert_file('wave_med.nc', 'wave')
    
    # Convertir datos bioquímicos
    converter.convert_file('copernicus_data.nc', 'bio')

if __name__ == "__main__":
    main()
