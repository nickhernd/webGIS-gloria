from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(title="Sistema de Monitoreo de Piscifactorías")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/")
async def read_root():
    """Ruta principal que sirve el index.html"""
    return FileResponse('public/views/index.html')

# Importar routers
from .routers import farms, weather, wave_data, alerts, pipeline

# Incluir routers
app.include_router(farms.router, prefix="/api")
app.include_router(weather.router, prefix="/api")
app.include_router(wave_data.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(pipeline.router, prefix="/api")
