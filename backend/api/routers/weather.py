from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
import json
from pathlib import Path
from datetime import datetime

router = APIRouter()

# Configuración de rutas de datos
DATA_DIR = Path("data")
PROCESSED_DIR = DATA_DIR / "processed"
WEATHER_DIR = PROCESSED_DIR / "weather"

@router.get("/weather-data")
async def get_weather_data() -> Dict[str, Any]:
    """
    Obtener datos meteorológicos actuales
    """
    try:
        weather_path = WEATHER_DIR / "weather_data.json"
        if not weather_path.exists():
            raise HTTPException(
                status_code=404, 
                detail="Datos meteorológicos no encontrados"
            )
            
        with open(weather_path) as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error leyendo datos meteorológicos: {str(e)}"
        )

@router.get("/weather-data/alerts")
async def get_weather_alerts() -> List[Dict[str, Any]]:
    """
    Obtener alertas meteorológicas activas
    """
    try:
        alerts_path = WEATHER_DIR / "weather_alerts.json"
        if not alerts_path.exists():
            return []  # Si no hay archivo de alertas, devolver lista vacía
            
        with open(alerts_path) as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error leyendo alertas meteorológicas: {str(e)}"
        )

@router.get("/weather-data/{farm_id}")
async def get_farm_weather(farm_id: str) -> Dict[str, Any]:
    """
    Obtener datos meteorológicos específicos de una piscifactoría
    """
    try:
        # Cargar datos meteorológicos de la piscifactoría específica
        farm_weather_path = WEATHER_DIR / f"farm_{farm_id}_weather.json"
        if not farm_weather_path.exists():
            raise HTTPException(
                status_code=404, 
                detail=f"Datos meteorológicos no encontrados para piscifactoría {farm_id}"
            )
            
        with open(farm_weather_path) as f:
            return json.load(f)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error leyendo datos meteorológicos de la piscifactoría: {str(e)}"
        )

@router.get("/weather-data/history/{farm_id}")
async def get_farm_weather_history(farm_id: str) -> Dict[str, Any]:
    """
    Obtener historial meteorológico de una piscifactoría
    """
    try:
        history_path = WEATHER_DIR / "history" / f"farm_{farm_id}_history.json"
        if not history_path.exists():
            raise HTTPException(
                status_code=404, 
                detail="Historial meteorológico no encontrado"
            )
            
        with open(history_path) as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error leyendo historial meteorológico: {str(e)}"
        )