"""
Módulo de Procesamiento de Anomalías

Detecta y procesa anomalías en datos oceanográficos y meteorológicos.
Convierte las anomalías detectadas a formato JSON para visualización.

Autor: Jaime Hernández
Actualizado: 2025
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, List, Optional
import logging
from pathlib import Path
from scipy import stats

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('logs/anomalies.log')]
)
logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self, data_dir: str = 'data/processed'):
        self.data_dir = Path(data_dir)
        self.threshold = 2  # Desviaciones estándar para considerar anomalía

    def detect_anomalies(self, df: pd.DataFrame, 
                        columns: List[str]) -> pd.DataFrame:
        """
        Detecta anomalías usando el método de Z-score.
        
        Args:
            df: DataFrame con datos
            columns: Columnas a analizar
        """
        df_anomalies = df.copy()
        
        for column in columns:
            z_scores = np.abs(stats.zscore(df[column]))
            df_anomalies[f'{column}_anomaly'] = z_scores > self.threshold
            
        return df_anomalies

    def load_data(self, filename: str) -> Optional[pd.DataFrame]:
        """Carga datos desde CSV."""
        try:
            return pd.read_csv(self.data_dir / filename)
        except Exception as e:
            logger.error(f"Error cargando datos: {str(e)}")
            return None

    def save_anomalies(self, df: pd.DataFrame, 
                      output_file: str) -> bool:
        """
        Guarda anomalías en formato JSON.
        
        Args:
            df: DataFrame con anomalías
            output_file: Archivo de salida
        """
        try:
            anomalies_dict = {
                'type': 'FeatureCollection',
                'features': []
            }

            for _, row in df.iterrows():
                if any(col for col in df.columns if col.endswith('_anomaly') 
                      and row[col]):
                    feature = {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [row['longitude'], row['latitude']]
                        },
                        'properties': {
                            'time': row['time'],
                            'anomalies': {
                                col.replace('_anomaly', ''): row[col]
                                for col in df.columns
                                if col.endswith('_anomaly')
                            }
                        }
                    }
                    anomalies_dict['features'].append(feature)

            with open(self.data_dir / output_file, 'w') as f:
                json.dump(anomalies_dict, f, indent=2)
            
            logger.info(f"Anomalías guardadas en {output_file}")
            return True

        except Exception as e:
            logger.error(f"Error guardando anomalías: {str(e)}")
            return False

def main():
    detector = AnomalyDetector()
    
    # Cargar datos
    df = detector.load_data('processed_data.csv')
    if df is None:
        return
    
    # Detectar anomalías en columnas específicas
    columns_to_analyze = ['VHM0', 'VMDR', 'VPED']  # Ejemplo de columnas
    df_anomalies = detector.detect_anomalies(df, columns_to_analyze)
    
    # Guardar resultados
    detector.save_anomalies(df_anomalies, 'anomalies.geojson')

if __name__ == "__main__":
    main()
