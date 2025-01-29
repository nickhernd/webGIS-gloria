"""
Módulo de Conversión de CSV a GeoJSON

Convierte datos procesados de CSV a formato GeoJSON para visualización en mapas.
Incluye funcionalidades para procesamiento temporal y espacial de datos.

Actualizado: 2024
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/geojson_conversion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GeoJSONConverter:
    def __init__(self, input_dir: str = 'data/temp', output_dir: str = 'data/processed'):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self._create_directories()

    def _create_directories(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _read_csv(self, file_path: Path) -> Optional[pd.DataFrame]:
        try:
            return pd.read_csv(file_path, parse_dates=['time'])
        except Exception as e:
            logger.error(f"Error al leer CSV {file_path}: {str(e)}")
            return None

    def _create_geojson_feature(self, row: pd.Series) -> Dict:
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(row['longitude']), float(row['latitude'])]
            },
            "properties": {
                "time": row['time'].isoformat(),
                **{col: float(val) for col, val in row.items() 
                   if col not in ['longitude', 'latitude', 'time']}
            }
        }

    def convert_to_geojson(self, input_file: str, output_file: str) -> bool:
        try:
            df = self._read_csv(self.input_dir / input_file)
            if df is None:
                return False

            features = [self._create_geojson_feature(row) for _, row in df.iterrows()]
            geojson = {
                "type": "FeatureCollection",
                "features": features
            }

            output_path = self.output_dir / output_file
            with open(output_path, 'w') as f:
                json.dump(geojson, f)

            logger.info(f"Archivo GeoJSON creado exitosamente: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error en la conversión a GeoJSON: {str(e)}")
            return False

    def convert_with_time_filter(self, input_file: str, output_file: str, 
                               start_date: datetime, end_date: datetime) -> bool:
        try:
            df = self._read_csv(self.input_dir / input_file)
            if df is None:
                return False

            mask = (df['time'] >= start_date) & (df['time'] <= end_date)
            df_filtered = df.loc[mask]

            features = [self._create_geojson_feature(row) for _, row in df_filtered.iterrows()]
            geojson = {
                "type": "FeatureCollection",
                "features": features
            }

            output_path = self.output_dir / output_file
            with open(output_path, 'w') as f:
                json.dump(geojson, f)

            logger.info(f"Archivo GeoJSON filtrado creado: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error en la conversión con filtro temporal: {str(e)}")
            return False

def main():
    converter = GeoJSONConverter()
    
    converter.convert_to_geojson(
        'wave_data.csv', 
        'wave_data.geojson'
    )
    
    converter.convert_to_geojson(
        'bio_data.csv', 
        'bio_data.geojson'
    )

if __name__ == "__main__":
    main()
