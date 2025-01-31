from typing import Dict, List, Any
import json
import numpy as np
from shapely.geometry import shape, Point
from shapely.ops import unary_union
import geopandas as gpd

def calculate_centers(geojson_data: Dict[str, Any]) -> List[Dict[str, float]]:
    """
    Calcula los centros de las piscifactorías desde datos GeoJSON.
    
    Args:
        geojson_data: Diccionario con datos GeoJSON de las piscifactorías
        
    Returns:
        Lista de diccionarios con las coordenadas de los centros
    """
    centers = []
    
    for feature in geojson_data['features']:
        # Crear geometría Shapely desde el feature
        geom = shape(feature['geometry'])
        
        # Calcular centroide
        center = geom.centroid
        
        # Añadir a la lista de centros
        centers.append({
            'id': feature['properties'].get('id', ''),
            'name': feature['properties'].get('name', ''),
            'lat': center.y,
            'lon': center.x
        })
    
    return centers

def process_geographic_data(input_path: str, output_path: str) -> bool:
    """
    Procesa datos geográficos y calcula centros.
    
    Args:
        input_path: Ruta al archivo GeoJSON de entrada
        output_path: Ruta donde guardar el resultado
        
    Returns:
        bool: True si el proceso fue exitoso
    """
    try:
        # Leer GeoJSON
        with open(input_path) as f:
            data = json.load(f)
        
        # Calcular centros
        centers = calculate_centers(data)
        
        # Añadir centros al GeoJSON original
        for feature, center in zip(data['features'], centers):
            feature['properties']['center'] = {
                'lat': center['lat'],
                'lon': center['lon']
            }
        
        # Guardar resultado
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"Error procesando datos geográficos: {str(e)}")
        return False

def calculate_buffer(geojson_data: Dict[str, Any], buffer_distance: float) -> Dict[str, Any]:
    """
    Calcula buffer alrededor de las piscifactorías.
    
    Args:
        geojson_data: Diccionario con datos GeoJSON
        buffer_distance: Distancia del buffer en metros
        
    Returns:
        Diccionario GeoJSON con los buffers calculados
    """
    try:
        # Convertir a GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])
        
        # Asegurar CRS correcto
        if gdf.crs is None:
            gdf.set_crs(epsg=4326, inplace=True)
        
        # Convertir a proyección métrica para el buffer
        gdf_projected = gdf.to_crs(epsg=3857)
        
        # Calcular buffer
        gdf_buffer = gdf_projected.buffer(buffer_distance)
        
        # Volver a WGS84
        gdf_buffer = gdf_buffer.to_crs(epsg=4326)
        
        # Crear nuevo GeoJSON
        buffer_features = []
        for idx, geom in enumerate(gdf_buffer):
            feature = {
                'type': 'Feature',
                'geometry': json.loads(gpd.GeoSeries([geom]).to_json())['features'][0]['geometry'],
                'properties': gdf.iloc[idx].to_dict()
            }
            buffer_features.append(feature)
        
        return {
            'type': 'FeatureCollection',
            'features': buffer_features
        }
        
    except Exception as e:
        print(f"Error calculando buffer: {str(e)}")
        return None

if __name__ == "__main__":
    # Ejemplo de uso
    import sys
    if len(sys.argv) > 2:
        process_geographic_data(sys.argv[1], sys.argv[2])
