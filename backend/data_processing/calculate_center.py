"""
Módulo de Cálculo de Centros Geográficos

Calcula los centroides de recintos y areas geográficas.
Procesa geometrías para análisis espacial.

Autor: Sebastian Pasker
Actualizado: 2024
"""

import geopandas as gpd
from shapely.geometry import Point, Polygon
import logging
from pathlib import Path
from typing import Optional, Dict, List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('logs/geometric_processing.log')]
)
logger = logging.getLogger(__name__)

class GeometryProcessor:
    def __init__(self, data_dir: str = 'data/processed'):
        self.data_dir = Path(data_dir)

    def calculate_centroid(self, geojson_file: str) -> Optional[gpd.GeoDataFrame]:
        """
        Calcula centroides para cada geometría en el GeoJSON.
        
        Args:
            geojson_file: Archivo GeoJSON de entrada
        """
        try:
            gdf = gpd.read_file(self.data_dir / geojson_file)
            gdf['geometry'] = gdf.geometry.centroid
            return gdf
        except Exception as e:
            logger.error(f"Error calculando centroides: {str(e)}")
            return None

    def save_processed_data(self, gdf: gpd.GeoDataFrame, output_file: str) -> bool:
        """
        Guarda GeoDataFrame procesado.
        
        Args:
            gdf: GeoDataFrame con centroides
            output_file: Archivo de salida
        """
        try:
            output_path = self.data_dir / output_file
            gdf.to_file(output_path, driver='GeoJSON')
            logger.info(f"Centroides guardados en {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error guardando centroides: {str(e)}")
            return False

    def add_buffer(self, gdf: gpd.GeoDataFrame, buffer_distance: float) -> gpd.GeoDataFrame:
        """
        Añade buffer alrededor de los centroides.
        
        Args:
            gdf: GeoDataFrame con centroides
            buffer_distance: Distancia del buffer en grados
        """
        try:
            gdf['geometry'] = gdf.geometry.buffer(buffer_distance)
            return gdf
        except Exception as e:
            logger.error(f"Error añadiendo buffer: {str(e)}")
            return gdf

def main():
    processor = GeometryProcessor()
    
    gdf = processor.calculate_centroid('recintos.geojson')
    if gdf is not None:
        gdf = processor.add_buffer(gdf, 0.01)
        processor.save_processed_data(gdf, 'recintos_center.geojson')

if __name__ == "__main__":
    main()
