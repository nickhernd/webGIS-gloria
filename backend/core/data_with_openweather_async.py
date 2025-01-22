import aiohttp
import asyncio
import geojson
import sys
from config_python import ConfigPath
from openweather_data import obtain_openweather_data_async


# Función asíncrona que se encarga de obtener los datos de openweather
async def run_async_main(coords):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(
            *(
                obtain_openweather_data_async(
                    coord, sys.argv[1], sys.argv[2], session
                )
                for coord in coords
            )
        )

        return ret


data_path = ConfigPath.data_path()
file_in = "recintos_with_data.geojson"
file_out = "recintos_with_openweather.geojson"

if len(sys.argv) != 3:
    print("Usage: python3 data_with_openweather.py <date> <hour>")
    exit()

with open(data_path + file_in, "r") as f:
    data = geojson.load(f)

coords = []
# Nos guardamos las coordenadas
for feature in data["features"]:
    coord = feature["properties"]["center"]
    coords.append(coord)

# Buscamos en base a unas coordenadas de forma asíncrona
weather_json = asyncio.run(run_async_main(coords))

# Guardamos la información
for i in range(0, len(data["features"])):
    data["features"][i]["properties"]["humidity"] = weather_json[i][
        "data"
    ][0]["humidity"]
    data["features"][i]["properties"]["temp"] = weather_json[i]["data"][
        0
    ]["temp"]
    data["features"][i]["properties"]["feels_like"] = weather_json[i][
        "data"
    ][0]["feels_like"]
    data["features"][i]["properties"]["wind_speed"] = weather_json[i][
        "data"
    ][0]["wind_speed"]
    data["features"][i]["properties"]["wind_deg"] = weather_json[i][
        "data"
    ][0]["wind_deg"]
    data["features"][i]["properties"]["visibility"] = weather_json[i][
        "data"
    ][0]["visibility"]
    data["features"][i]["properties"]["pressure"] = weather_json[i][
        "data"
    ][0]["pressure"]
    data["features"][i]["properties"]["clouds"] = weather_json[i][
        "data"
    ][0]["clouds"]


with open(data_path + file_out, "w") as f:
    geojson.dump(data, f)
