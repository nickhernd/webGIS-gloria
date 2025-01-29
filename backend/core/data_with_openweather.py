"""
Módulo de Integración con OpenWeather

Obtiene y procesa datos meteorológicos de la API de OpenWeather.
Integra información meteorológica con datos geográficos existentes.

Autor: Sebastian Pasker
Actualizado: 2024
"""

import os
import json
import requests
from typing import Dict, List, Optional
import logging
from pathlib import Path
import asyncio
import aiohttp
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('logs/weather_data.log')]
)
logger = logging.getLogger(__name__)

class WeatherDataFetcher:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise EnvironmentError("API_KEY de OpenWeather no encontrada")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    async def fetch_weather_data(self, session: aiohttp.ClientSession, 
                               lat: float, lon: float) -> Optional[Dict]:
        """
        Obtiene datos meteorológicos de forma asíncrona.
        
        Args:
            session: Sesión aiohttp
            lat: Latitud
            lon: Longitud
        """
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }

        try:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_weather_data(data)
                else:
                    logger.error(f"Error API: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error en petición: {str(e)}")
            return None

    def _process_weather_data(self, data: Dict) -> Dict:
        """
        Procesa datos meteorológicos crudos.
        
        Args:
            data: Datos de la API
        """
        return {
            'temperatura': data['main']['temp'],
            'sensacion_termica': data['main']['feels_like'],
            'humedad': data['main']['humidity'],
            'presion': data['main']['pressure'],
            'velocidad_viento': data['wind']['speed'],
            'direccion_viento': data.get('wind', {}).get('deg', 0),
            'nubosidad': data['clouds']['all'],
            'visibilidad': data.get('visibility', 0)
        }

    async def fetch_multiple_locations(self, locations: List[Dict[str, float]]) -> List[Dict]:
        """
        Obtiene datos para múltiples ubicaciones.
        
        Args:
            locations: Lista de diccionarios con lat/lon
        """
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_weather_data(session, loc['lat'], loc['lon'])
                for loc in locations
            ]
            results = await asyncio.gather(*tasks)
            
            processed_data = []
            for loc, result in zip(locations, results):
                if result:
                    processed_data.append({
                        'latitude': loc['lat'],
                        'longitude': loc['lon'],
                        'weather_data': result
                    })
            
            return processed_data

    def save_weather_data(self, data: List[Dict], output_file: str):
        """
        Guarda datos meteorológicos procesados.
        
        Args:
            data: Datos a guardar
            output_file: Ruta del archivo
        """
        try:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Datos guardados en {output_file}")
        except Exception as e:
            logger.error(f"Error guardando datos: {str(e)}")

def main():
    fetcher = WeatherDataFetcher()
    locations = [
        {'lat': 38.5, 'lon': -0.5},
        {'lat': 39.0, 'lon': -0.3}
    ]
    
    loop = asyncio.get_event_loop()
    weather_data = loop.run_until_complete(
        fetcher.fetch_multiple_locations(locations)
    )
    
    fetcher.save_weather_data(
        weather_data, 
        'data/processed/weather_data.json'
    )

if __name__ == "__main__":
    main()
