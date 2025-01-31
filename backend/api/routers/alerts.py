from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Any
import json
from pathlib import Path
from datetime import datetime

router = APIRouter()

# Configuración de rutas de datos
DATA_DIR = Path("data")
PROCESSED_DIR = DATA_DIR / "processed"
ANALYSIS_DIR = PROCESSED_DIR / "analysis"
WEATHER_DIR = PROCESSED_DIR / "weather"

@router.get("/alerts")
async def get_all_alerts() -> List[Dict[str, Any]]:
    """
    Obtener todas las alertas activas
    """
    try:
        alerts = []
        
        # Obtener alertas de oleaje
        wave_alerts_path = ANALYSIS_DIR / "wave_alerts.json"
        if wave_alerts_path.exists():
            with open(wave_alerts_path) as f:
                wave_alerts = json.load(f)
                for alert in wave_alerts:
                    alert['type'] = 'wave'
                alerts.extend(wave_alerts)
        
        # Obtener alertas meteorológicas
        weather_alerts_path = WEATHER_DIR / "weather_alerts.json"
        if weather_alerts_path.exists():
            with open(weather_alerts_path) as f:
                weather_alerts = json.load(f)
                for alert in weather_alerts:
                    alert['type'] = 'weather'
                alerts.extend(weather_alerts)
                
        return alerts
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo alertas: {str(e)}"
        )

@router.get("/alerts/farm/{farm_id}")
async def get_farm_alerts(farm_id: str) -> List[Dict[str, Any]]:
    """
    Obtener alertas específicas de una piscifactoría
    """
    try:
        alerts = []
        
        # Obtener alertas de oleaje específicas
        farm_alerts_path = ANALYSIS_DIR / f"farm_{farm_id}_alerts.json"
        if farm_alerts_path.exists():
            with open(farm_alerts_path) as f:
                alerts.extend(json.load(f))
                
        return alerts
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo alertas de la piscifactoría: {str(e)}"
        )

@router.get("/alerts/history")
async def get_alerts_history(
    days: int = Query(default=7, le=30)
) -> List[Dict[str, Any]]:
    """
    Obtener historial de alertas
    """
    try:
        history_path = ANALYSIS_DIR / "alerts_history.json"
        if not history_path.exists():
            return []
            
        with open(history_path) as f:
            history = json.load(f)
            
        # Filtrar por número de días
        cutoff_date = datetime.now() - timedelta(days=days)
        filtered_history = [
            alert for alert in history
            if datetime.fromisoformat(alert['timestamp']) >= cutoff_date
        ]
            
        return filtered_history
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo historial de alertas: {str(e)}"
        )

@router.get("/alerts/stats")
async def get_alerts_stats() -> Dict[str, Any]:
    """
    Obtener estadísticas de alertas
    """
    try:
        stats_path = ANALYSIS_DIR / "alerts_stats.json"
        if not stats_path.exists():
            return {
                "total_alerts": 0,
                "active_alerts": 0,
                "by_type": {},
                "by_severity": {}
            }
            
        with open(stats_path) as f:
            return json.load(f)
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo estadísticas de alertas: {str(e)}"
        )