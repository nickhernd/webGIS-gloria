import asyncio
import geojson
import sys
from config_python import ConfigPath
from openweather_data import obtain_openweather_data


async def run_async_main(data):
    tasks = []
    for feature in data["features"]:
        coord = feature["properties"]["center"]

        task = asyncio.create_task(run_async(feature, coord))
        tasks.append(task)

    for task in tasks:
        await task


async def run_async(feature, coord):
    weather_json = obtain_openweather_data(
        coord, sys.argv[1], sys.argv[2]
    )

    feature["properties"]["humidity"] = weather_json["data"][0][
        "humidity"
    ]
    feature["properties"]["temp"] = weather_json["data"][0]["temp"]
    feature["properties"]["feels_like"] = weather_json["data"][0][
        "feels_like"
    ]
    feature["properties"]["wind_speed"] = weather_json["data"][0][
        "wind_speed"
    ]
    feature["properties"]["wind_deg"] = weather_json["data"][0][
        "wind_deg"
    ]
    feature["properties"]["visibility"] = weather_json["data"][0][
        "visibility"
    ]
    feature["properties"]["pressure"] = weather_json["data"][0][
        "pressure"
    ]
    feature["properties"]["clouds"] = weather_json["data"][0]["clouds"]


data_path = ConfigPath.data_path()
file_in = "recintos_with_data.geojson"
file_out = "recintos_with_openweather.geojson"

if len(sys.argv) != 3:
    print("Usage: python3 data_with_openweather.py <date> <hour>")
    exit()

with open(data_path + file_in, "r") as f:
    data = geojson.load(f)

asyncio.run(run_async_main(data))

with open(data_path + file_out, "w") as f:
    geojson.dump(data, f)
