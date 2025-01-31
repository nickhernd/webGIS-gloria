from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Any
import json
from pathlib import Path
from datetime import datetime, timedelta

router = APIRouter()

# Configuración de rutas de datos
DATA_DIR = Path("data")
PROCESSED_DIR = DATA_DIR / "processed"
DAILY_DIR = PROCESSED_DIR / "daily"
ANALYSIS_DIR = PROCESSED_DIR / "analysis"

@router.get("/wave-data")
async def get_wave_data() -> Dict[str, Any]:
    """
    Obtener datos actuales de oleaje
    """
    try:
        current_date = datetime.now().strftime('%Y-%m-%d')
        wave_path = DAILY_DIR / "data_by_date" / f"data-{current_date}.geojson"
        
        if not wave_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Datos de oleaje no encontrados"
            )
            
        with open(wave_path) as f:
            data = json.load(f)
            
        # Procesar datos para el formato requerido
        processed_data = {
            "labels": [],
            "values": []
        }
        
        # Extraer datos de las últimas 24 horas
        for feature in data['features']:
            if 'properties' in feature:
                props = feature['properties']
                processed_data['labels'].append(props.get('time', ''))
                processed_data['values'].append(props.get('wave_height', 0))
                
        return processed_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo datos de oleaje: {str(e)}"
        )

@router.get("/wave-data/history")
async def get_wave_history(
    days: int = Query(default=7, le=30)
) -> List[Dict[str, Any]]:
    """
    Obtener historial de datos de oleaje
    """
    try:
        history_data = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Recopilar datos para cada día
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            daily_path = DAILY_DIR / "data_by_date" / f"data-{date_str}.geojson"
            
            if daily_path.exists():
                with open(daily_path) as f:
                    data = json.load(f)
                    history_data.append({
                        'date': date_str,
                        'data': data
                    })
                    
            current_date += timedelta(days=1)
            
        return history_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo historial de oleaje: {str(e)}"
        )

@router.get("/wave-data/farm/{farm_id}")
async def get_farm_wave_data(farm_id: str) -> Dict[str, Any]:
    """
    Obtener datos de oleaje específicos de una piscifactoría
    """
    try:
        # Cargar datos del día actual
        current_date = datetime.now().strftime('%Y-%m-%d')
        wave_path = DAILY_DIR / "data_by_date" / f"data-{current_date}.geojson"
        
        if not wave_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Datos de oleaje no encontrados"
            )
            
        with open(wave_path) as f:
            data = json.load(f)
            
        # Buscar datos específicos de la piscifactoría
        farm_data = None
        for feature in data['features']:
            if feature['properties'].get('farm_id') == farm_id:
                farm_data = feature['properties']
                break
                
        if not farm_data:
            raise HTTPException(
                status_code=404,
                detail=f"Datos no encontrados para piscifactoría {farm_id}"
            )
            
        return farm_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo datos de oleaje: {str(e)}"
        )

@router.get("/wave-data/analysis/{farm_id}")
async def get_wave_analysis(farm_id: str) -> Dict[str, Any]:
    """
    Obtener análisis de datos de oleaje para una piscifactoría
    """
    try:
        analysis_path = ANALYSIS_DIR / f"wave_analysis_{farm_id}.json"
        
        if not analysis_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Análisis de oleaje no encontrado"
            )
            
        with open(analysis_path) as f:
            return json.load(f)
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo análisis de oleaje: {str(e)}"
        )