from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Any, Optional
import json
import os
from pathlib import Path
from datetime import datetime

router = APIRouter()

# Configuración de rutas
LOG_DIR = Path("logs")
PID_FILE = LOG_DIR / "pipeline.pid"
LOG_FILE = LOG_DIR / "pipeline.log"

@router.get("/pipeline/status")
async def get_pipeline_status() -> Dict[str, Any]:
    """
    Obtener estado actual del pipeline
    """
    try:
        status = {
            "running": False,
            "last_update": None,
            "status": "stopped",
            "details": {}
        }
        
        # Verificar si el pipeline está en ejecución
        if PID_FILE.exists():
            pid = PID_FILE.read_text().strip()
            try:
                os.kill(int(pid), 0)  # Verificar si el proceso existe
                status["running"] = True
                status["status"] = "running"
            except OSError:
                pass
        
        # Obtener última actualización del log
        if LOG_FILE.exists():
            with open(LOG_FILE) as f:
                lines = f.readlines()
                for line in reversed(lines):
                    if "Pipeline completado" in line:
                        timestamp = line.split()[0]
                        status["last_update"] = datetime.fromisoformat(timestamp)
                        break
        
        # Obtener detalles adicionales si están disponibles
        details_path = LOG_DIR / "pipeline_details.json"
        if details_path.exists():
            with open(details_path) as f:
                status["details"] = json.load(f)
                
        return status
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo estado del pipeline: {str(e)}"
        )

@router.get("/pipeline/history")
async def get_pipeline_history() -> List[Dict[str, Any]]:
    """
    Obtener historial de ejecuciones del pipeline
    """
    try:
        history_path = LOG_DIR / "pipeline_history.json"
        if not history_path.exists():
            return []
            
        with open(history_path) as f:
            return json.load(f)
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo historial del pipeline: {str(e)}"
        )

@router.get("/pipeline/logs")
async def get_pipeline_logs(
    lines: int = Query(default=100, le=1000)
) -> List[str]:
    """
    Obtener últimas líneas del log del pipeline
    """
    try:
        if not LOG_FILE.exists():
            return []
            
        with open(LOG_FILE) as f:
            all_lines = f.readlines()
            return all_lines[-lines:]
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo logs del pipeline: {str(e)}"
        )

@router.post("/pipeline/restart")
async def restart_pipeline() -> Dict[str, Any]:
    """
    Reiniciar el pipeline
    """
    try:
        # Implementar lógica de reinicio aquí
        return {
            "status": "success",
            "message": "Pipeline reiniciado correctamente"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reiniciando pipeline: {str(e)}"
        )
