from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import json
from pathlib import Path
from datetime import datetime

router = APIRouter()

# Configuración de rutas de datos
DATA_DIR = Path("data")
PROCESSED_DIR = DATA_DIR / "processed"
GEOGRAPHIC_DIR = PROCESSED_DIR / "geographic"

@router.get("/farms/geojson")
async def get_farms_geojson() -> Dict[str, Any]:
    """
    Obtener datos GeoJSON de todas las piscifactorías
    """
    try:
        geojson_path = GEOGRAPHIC_DIR / "recintos_with_data_center.geojson"
        if not geojson_path.exists():
            raise HTTPException(
                status_code=404, 
                detail="Archivo GeoJSON no encontrado"
            )
            
        with open(geojson_path) as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error leyendo datos GeoJSON: {str(e)}"
        )

@router.get("/farms/{farm_id}")
async def get_farm_details(farm_id: str) -> Dict[str, Any]:
    """
    Obtener detalles específicos de una piscifactoría
    """
    try:
        geojson_path = GEOGRAPHIC_DIR / "recintos_with_data_center.geojson"
        if not geojson_path.exists():
            raise HTTPException(
                status_code=404, 
                detail="Datos de piscifactorías no encontrados"
            )
            
        with open(geojson_path) as f:
            data = json.load(f)
            
        # Buscar la piscifactoría específica
        for feature in data['features']:
            if feature['properties'].get('id') == farm_id:
                return feature['properties']
                
        raise HTTPException(
            status_code=404, 
            detail=f"Piscifactoría con ID {farm_id} no encontrada"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error leyendo datos de la piscifactoría: {str(e)}"
        )

@router.get("/farms/{farm_id}/data")
async def get_farm_data(farm_id: str) -> Dict[str, Any]:
    """
    Obtener datos históricos de una piscifactoría específica
    """
    try:
        farm_data_path = PROCESSED_DIR / "analysis" / f"farm_{farm_id}.json"
        if not farm_data_path.exists():
            raise HTTPException(
                status_code=404, 
                detail="Datos históricos no encontrados"
            )
            
        with open(farm_data_path) as f:
            return json.load(f)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error leyendo datos históricos: {str(e)}"
        )

@router.get("/farms/{farm_id}/status")
async def get_farm_status(farm_id: str) -> Dict[str, Any]:
    """
    Obtener estado actual de una piscifactoría específica
    """
    try:
        # Obtener datos del último día
        current_date = datetime.now().strftime('%Y-%m-%d')
        daily_data_path = PROCESSED_DIR / "daily" / "data_by_date" / f"data-{current_date}.geojson"
        
        if not daily_data_path.exists():
            raise HTTPException(
                status_code=404, 
                detail="Datos actuales no encontrados"
            )
            
        with open(daily_data_path) as f:
            data = json.load(f)
            
        # Buscar datos de la piscifactoría específica
        for feature in data['features']:
            if feature['properties'].get('farm_id') == farm_id:
                return {
                    'timestamp': feature['properties'].get('timestamp'),
                    'wave_height': feature['properties'].get('wave_height'),
                    'temperature': feature['properties'].get('temperature'),
                    'status': feature['properties'].get('status', 'unknown')
                }
                
        raise HTTPException(
            status_code=404, 
            detail=f"Estado actual no encontrado para la piscifactoría {farm_id}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error leyendo estado actual: {str(e)}"
        )