"""
Módulo de Obtención de Datos OpenWeather

Gestiona la obtención y procesamiento de datos meteorológicos de OpenWeather.
Incluye funcionalidades para datos actuales y pronósticos.

Autor: Sebastian Pasker
Actualizado: 2024
"""

import os
import json
import aiohttp
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   handlers=[logging.FileHandler('logs/weather_api.log')]
)
logger = logging.getLogger(__name__)

class OpenWeatherAPI:
   def __init__(self):
       self.api_key = os.getenv('OPENWEATHER_API_KEY')
       if not self.api_key:
           raise EnvironmentError("API_KEY de OpenWeather no encontrada")
       
       self.base_url = "http://api.openweathermap.org/data/2.5"
       self.output_dir = Path('data/processed/weather')
       self.output_dir.mkdir(parents=True, exist_ok=True)

   async def get_current_weather(self, session: aiohttp.ClientSession, 
                               lat: float, lon: float) -> Optional[Dict]:
       """
       Obtiene datos meteorológicos actuales.
       
       Args:
           session: Sesión aiohttp
           lat: Latitud
           lon: Longitud
       """
       try:
           params = {
               'lat': lat,
               'lon': lon,
               'appid': self.api_key,
               'units': 'metric',
               'lang': 'es'
           }
           
           async with session.get(f"{self.base_url}/weather", params=params) as response:
               if response.status == 200:
                   data = await response.json()
                   return self._process_current_weather(data)
               else:
                   logger.error(f"Error API: {response.status}")
                   return None
                   
       except Exception as e:
           logger.error(f"Error obteniendo datos actuales: {str(e)}")
           return None

   async def get_forecast(self, session: aiohttp.ClientSession, 
                        lat: float, lon: float) -> Optional[Dict]:
       """
       Obtiene pronóstico meteorológico.
       
       Args:
           session: Sesión aiohttp
           lat: Latitud
           lon: Longitud
       """
       try:
           params = {
               'lat': lat,
               'lon': lon,
               'appid': self.api_key,
               'units': 'metric',
               'lang': 'es'
           }
           
           async with session.get(f"{self.base_url}/forecast", params=params) as response:
               if response.status == 200:
                   data = await response.json()
                   return self._process_forecast(data)
               else:
                   logger.error(f"Error API pronóstico: {response.status}")
                   return None
                   
       except Exception as e:
           logger.error(f"Error obteniendo pronóstico: {str(e)}")
           return None

   def _process_current_weather(self, data: Dict) -> Dict:
       """
       Procesa datos meteorológicos actuales.
       
       Args:
           data: Datos crudos de la API
       """
       return {
           'temperatura': data['main']['temp'],
           'sensacion_termica': data['main']['feels_like'],
           'humedad': data['main']['humidity'],
           'presion': data['main']['pressure'],
           'velocidad_viento': data['wind']['speed'],
           'direccion_viento': data.get('wind', {}).get('deg', 0),
           'descripcion': data['weather'][0]['description'],
           'nubosidad': data['clouds']['all'],
           'visibilidad': data.get('visibility', 0),
           'timestamp': datetime.now().isoformat()
       }

   def _process_forecast(self, data: Dict) -> List[Dict]:
       """
       Procesa datos de pronóstico.
       
       Args:
           data: Datos crudos de pronóstico
       """
       forecast_data = []
       for item in data['list']:
           forecast_data.append({
               'timestamp': item['dt_txt'],
               'temperatura': item['main']['temp'],
               'sensacion_termica': item['main']['feels_like'],
               'humedad': item['main']['humidity'],
               'presion': item['main']['pressure'],
               'velocidad_viento': item['wind']['speed'],
               'direccion_viento': item['wind'].get('deg', 0),
               'descripcion': item['weather'][0]['description'],
               'nubosidad': item['clouds']['all']
           })
       return forecast_data

   async def process_locations(self, locations: List[Dict[str, float]]) -> Dict:
       """
       Procesa múltiples ubicaciones.
       
       Args:
           locations: Lista de ubicaciones {lat, lon}
       """
       async with aiohttp.ClientSession() as session:
           tasks = []
           for loc in locations:
               tasks.append(self.get_current_weather(session, loc['lat'], loc['lon']))
               tasks.append(self.get_forecast(session, loc['lat'], loc['lon']))
           
           results = await asyncio.gather(*tasks)
           
           processed_data = {}
           for i, loc in enumerate(locations):
               loc_key = f"{loc['lat']},{loc['lon']}"
               processed_data[loc_key] = {
                   'current': results[i*2],
                   'forecast': results[i*2 + 1]
               }
           
           return processed_data

   def save_weather_data(self, data: Dict, filename: str) -> bool:
       """
       Guarda datos meteorológicos procesados.
       
       Args:
           data: Datos a guardar
           filename: Nombre del archivo
       """
       try:
           output_path = self.output_dir / filename
           with open(output_path, 'w') as f:
               json.dump(data, f, indent=2)
           logger.info(f"Datos guardados en {output_path}")
           return True
       except Exception as e:
           logger.error(f"Error guardando datos: {str(e)}")
           return False

async def main():
   api = OpenWeatherAPI()
   
   locations = [
       {'lat': 38.5, 'lon': -0.5},  # Ejemplo de ubicaciones
       {'lat': 39.0, 'lon': -0.3}
   ]
   
   weather_data = await api.process_locations(locations)
   api.save_weather_data(weather_data, 'weather_data.json')

if __name__ == "__main__":
   asyncio.run(main())
