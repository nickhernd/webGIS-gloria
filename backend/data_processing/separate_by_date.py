import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def separate_data_by_date(input_file: str, output_dir: str) -> bool:
    """
    Separa los datos en archivos diferentes por fecha.
    
    Args:
        input_file: Ruta al archivo CSV de entrada
        output_dir: Directorio donde guardar los archivos separados
        
    Returns:
        bool: True si el proceso fue exitoso
    """
    try:
        # Crear directorio de salida si no existe
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Leer datos
        df = pd.read_csv(input_file)
        
        # Asegurarse de que existe la columna de fecha
        if 'date' not in df.columns and 'timestamp' not in df.columns:
            raise ValueError("No se encontró columna de fecha en los datos")
        
        date_column = 'date' if 'date' in df.columns else 'timestamp'
        
        # Convertir a datetime si no lo es ya
        df[date_column] = pd.to_datetime(df[date_column])
        
        # Agrupar por fecha
        grouped = df.groupby(df[date_column].dt.date)
        
        # Crear un archivo GeoJSON para cada fecha
        for date, group in grouped:
            # Crear features para cada fila
            features = []
            for _, row in group.iterrows():
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [row['longitude'], row['latitude']]
                    },
                    "properties": row.drop(['longitude', 'latitude']).to_dict()
                }
                features.append(feature)
            
            # Crear GeoJSON
            geojson = {
                "type": "FeatureCollection",
                "features": features
            }
            
            # Guardar archivo
            output_file = output_path / f"data-{date}.geojson"
            with open(output_file, 'w') as f:
                json.dump(geojson, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"Error separando datos por fecha: {str(e)}")
        return False

def process_date_range(start_date: str, end_date: str, data_dir: str) -> List[Dict[str, Any]]:
    """
    Procesa datos para un rango de fechas.
    
    Args:
        start_date: Fecha inicial (YYYY-MM-DD)
        end_date: Fecha final (YYYY-MM-DD)
        data_dir: Directorio con los archivos de datos
        
    Returns:
        Lista de datos procesados para el rango
    """
    try:
        data_path = Path(data_dir)
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        processed_data = []
        
        # Buscar archivos en el rango de fechas
        for date_file in data_path.glob('data-*.geojson'):
            file_date = datetime.strptime(
                date_file.stem.replace('data-', ''), 
                '%Y-%m-%d'
            ).date()
            
            if start <= file_date <= end:
                with open(date_file) as f:
                    data = json.load(f)
                    processed_data.append({
                        'date': str(file_date),
                        'data': data
                    })
        
        return sorted(processed_data, key=lambda x: x['date'])
        
    except Exception as e:
        print(f"Error procesando rango de fechas: {str(e)}")
        return []

def merge_date_data(data_dir: str, output_file: str) -> bool:
    """
    Combina datos de diferentes fechas en un solo archivo.
    
    Args:
        data_dir: Directorio con los archivos de datos
        output_file: Archivo de salida
        
    Returns:
        bool: True si el proceso fue exitoso
    """
    try:
        data_path = Path(data_dir)
        all_features = []
        
        # Leer todos los archivos
        for date_file in sorted(data_path.glob('data-*.geojson')):
            with open(date_file) as f:
                data = json.load(f)
                all_features.extend(data['features'])
        
        # Crear GeoJSON combinado
        combined_geojson = {
            "type": "FeatureCollection",
            "features": all_features
        }
        
        # Guardar resultado
        with open(output_file, 'w') as f:
            json.dump(combined_geojson, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"Error combinando datos: {str(e)}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        separate_data_by_date(sys.argv[1], sys.argv[2])
