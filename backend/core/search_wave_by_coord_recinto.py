"""
Módulo de Búsqueda de Datos por Coordenadas

Encuentra y procesa datos de oleaje cerca de recintos específicos.
Utiliza algoritmos de proximidad espacial para asociar datos.

Autor: Sebastian Pasker
Actualizado: 2024
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point
from typing import List, Dict, Optional
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('logs/spatial_search.log')]
)
logger = logging.getLogger(__name__)

class WaveDataSearcher:
    def __init__(self, data_dir: str = 'data/processed'):
        self.data_dir = Path(data_dir)
        self.earth_radius = 6371  # km

    def _load_geojson(self, filename: str) -> Optional[gpd.GeoDataFrame]:
        try:
            filepath = self.data_dir / filename
            return gpd.read_file(filepath)
        except Exception as e:
            logger.error(f"Error cargando GeoJSON {filename}: {str(e)}")
            return None

    def _calculate_distances(self, point: Point, points_df: gpd.GeoDataFrame) -> np.ndarray:
        """Calcula distancias entre un punto y conjunto de puntos."""
        return points_df.geometry.distance(point) * self.earth_radius

    def find_nearest_waves(self, recintos_file: str, waves_file: str, 
                         max_distance: float = 5.0) -> Optional[gpd.GeoDataFrame]:
        """
        Encuentra datos de oleaje más cercanos a recintos.
        
        Args:
            recintos_file: Archivo GeoJSON de recintos
            waves_file: Archivo GeoJSON de datos de oleaje
            max_distance: Distancia máxima en km
        """
        try:
            recintos_gdf = self._load_geojson(recintos_file)
            waves_gdf = self._load_geojson(waves_file)
            
            if recintos_gdf is None or waves_gdf is None:
                return None

            results = []
            for idx, recinto in recintos_gdf.iterrows():
                distances = self._calculate_distances(recinto.geometry, waves_gdf)
                nearest_idx = distances.argmin()
                
                if distances[nearest_idx] <= max_distance:
                    wave_data = waves_gdf.iloc[nearest_idx].copy()
                    wave_data['recinto_id'] = recinto['id']
                    wave_data['distance'] = distances[nearest_idx]
                    results.append(wave_data)

            if results:
                return gpd.GeoDataFrame(results)
            return None

        except Exception as e:
            logger.error(f"Error en búsqueda de oleaje: {str(e)}")
            return None

    def save_results(self, gdf: gpd.GeoDataFrame, output_file: str) -> bool:
        """
        Guarda resultados en formato GeoJSON.
        
        Args:
            gdf: GeoDataFrame con resultados
            output_file: Nombre del archivo de salida
        """
        try:
            output_path = self.data_dir / output_file
            gdf.to_file(output_path, driver='GeoJSON')
            logger.info(f"Resultados guardados en {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error guardando resultados: {str(e)}")
            return False

def main():
    searcher = WaveDataSearcher()
    results = searcher.find_nearest_waves(
        'recintos.geojson',
        'wave_data.geojson'
    )
    
    if results is not None:
        searcher.save_results(results, 'wave_by_recinto.geojson')

if __name__ == "__main__":
    main()







































