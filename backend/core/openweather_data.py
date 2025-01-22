"""
    Script para llamar información de openweather
    en base a unas coordenadas, fecha y hora.
"""

from datetime import datetime
import requests
import time
from config_python import ConfigPath


def obtain_openweather_data(coord, date_str, time_str):
    api_key = ConfigPath.api_openweather()
    url = "https://api.openweathermap.org/data/3.0/onecall/timemachine?"
    # timezone = "+01:00"
    url_var = "lat={lat}&lon={lon}&appid={api_key}&dt={timestamp}&units=metric"
    date = datetime.strptime(
        date_str + " " + time_str, "%Y-%m-%d %H:%M"
    )

    # Creamos el timestamp con mktime
    timestamp = str(time.mktime(date.timetuple()))

    url = url + url_var.format(
        lat=str(coord[1]),
        lon=str(coord[0]),
        timestamp=str(timestamp)[:-2],
        api_key=api_key,
    )

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


async def obtain_openweather_data_async(
    coord, date_str, time_str, session
):
    api_key = ConfigPath.api_openweather()
    url = "https://api.openweathermap.org/data/3.0/onecall/timemachine?"
    url_var = "lat={lat}&lon={lon}&appid={api_key}&dt={timestamp}&units=metric"
    date = datetime.strptime(
        date_str + " " + time_str, "%Y-%m-%d %H:%M"
    )

    # Creamos el timestamp con mktime
    timestamp = str(time.mktime(date.timetuple()))

    # Creamos la url
    url = url + url_var.format(
        lat=str(coord[1]),
        lon=str(coord[0]),
        timestamp=str(timestamp)[:-2],
        api_key=api_key,
    )

    try:
        # Realizamos la petición
        async with session.get(url) as response:
            return await response.json()
    except Exception as e:
        raise e
