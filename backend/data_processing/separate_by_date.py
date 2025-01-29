"""
Módulo de Separación de Datos por Fecha

Separa y organiza datos GeoJSON por fechas específicas.
Autor: Jaime Hernández
"""

import json
from datetime import datetime
import logging
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import geopandas as gpd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('logs/date_processing.log')]
)
logger = logging.getLogger(__name__)

class DateSeparator:
    def __init__(self, data_dir: str = 'data/processed'):
        self.data_dir = Path(data_dir)
        self.output_dir = self.data_dir / 'by_date'
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def separate_geojson(self, input_file: str) -> bool:
        try:
            with open(self.data_dir / input_file) as f:
                data = json.load(f)

            grouped_features = self._group_by_date(data['features'])
            return self._save_separate_files(grouped_features)
        except Exception as e:
            logger.error(f"Error en separación: {str(e)}")
            return False

    def _group_by_date(self, features: List[Dict]) -> Dict[str, List[Dict]]:
        grouped = {}
        for feature in features:
            date = feature['properties']['time'].split('T')[0]
            if date not in grouped:
                grouped[date] = []
            grouped[date].append(feature)
        return grouped

    def _save_separate_files(self, grouped_features: Dict[str, List[Dict]]) -> bool:
        try:
            for date, features in grouped_features.items():
                output_file = self.output_dir / f'data-{date}.geojson'
                geojson = {
                    "type": "FeatureCollection",
                    "features": features
                }
                with open(output_file, 'w') as f:
                    json.dump(geojson, f)
                logger.info(f"Creado archivo para fecha {date}")
            return True
        except Exception as e:
            logger.error(f"Error guardando archivos: {str(e)}")
            return False

def main():
    separator = DateSeparator()
    separator.separate_geojson('processed_data.geojson')

if __name__ == "__main__":
    main()
