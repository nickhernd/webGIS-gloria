"""
Inicialización de routers de la API
"""
from . import pipeline
from . import wave_data
from . import farms
from . import weather
from . import alerts

__all__ = ['pipeline', 'wave_data', 'farms', 'weather', 'alerts']
