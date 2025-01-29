"""
Módulo de Ordenamiento por Puntos Geográficos

Organiza datos CSV por coordenadas geográficas y realiza análisis espacial.
Permite agrupar y filtrar datos por proximidad a puntos de interés.

Autor: Jaime Hernández
Actualizado: 2024
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from typing import List, Dict, Optional
import logging
from pathlib import Path
import numpy as np
from sklearn.neighbors import BallTree

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('logs/spatial_processing.log')]
)
logger = logging.getLogger(__name__)

class SpatialDataProcessor:
    def __init__(self, data_dir: str = 'data/temp'):
        self.data_dir = Path(data_dir)
        self.earth_radius = 6371  # km

    def _haversine_distance(self, lat1: float, lon1: float, 
                          lat2: float, lon2: float) -> float:
        """Calcula distancia Haversine entre dos puntos."""
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        return 2 * self.earth_radius * np.arcsin(np.sqrt(a))

    def find_nearest_points(self, df: pd.DataFrame, 
                          target_points: List[Dict[str, float]], 
                          max_distance: float = 5.0) -> pd.DataFrame:
        """
        Encuentra puntos más cercanos a ubicaciones objetivo.
        
        Args:
            df: DataFrame con columnas 'latitude' y 'longitude'
            target_points: Lista de diccionarios con coordenadas objetivo
            max_distance: Distancia máxima en kilómetros
        """
        try:
            coords = df[['latitude', 'longitude']].values
            target_coords = np.array([[p['latitude'], p['longitude']] 
                                    for p in target_points])
            
            tree = BallTree(np.radians(coords), metric='haversine')
            distances, indices = tree.query(np.radians(target_coords))
            
            distances = distances.flatten() * self.earth_radius
            indices = indices.flatten()
            
            mask = distances <= max_distance
            nearest_df = df.iloc[indices[mask]].copy()
            nearest_df['distance'] = distances[mask]
            
            return nearest_df

        except Exception as e:
            logger.error(f"Error en búsqueda de puntos cercanos: {str(e)}")
            return pd.DataFrame()

    def process_file(self, filename: str, 
                    target_points: List[Dict[str, float]], 
                    output_filename: str) -> bool:
        """
        Procesa archivo CSV y guarda resultados filtrados.
        
        Args:
            filename: Nombre del archivo CSV
            target_points: Puntos objetivo
            output_filename: Nombre del archivo de salida
        """
        try:
            df = pd.read_csv(self.data_dir / filename)
            nearest_df = self.find_nearest_points(df, target_points)
            
            if not nearest_df.empty:
                output_path = self.data_dir / output_filename
                nearest_df.to_csv(output_path, index=False)
                logger.info(f"Datos procesados guardados en {output_path}")
                return True
            
            return False

        except Exception as e:
            logger.error(f"Error en procesamiento de archivo: {str(e)}")
            return False

def main():
    processor = SpatialDataProcessor()
    target_points = [
        {'latitude': 38.5, 'longitude': -0.5},
        {'latitude': 39.0, 'longitude': -0.3}
    ]
    
    processor.process_file(
        'wave_data.csv',
        target_points,
        'wave_data_ordered.csv'
    )

if __name__ == "__main__":
    main()
