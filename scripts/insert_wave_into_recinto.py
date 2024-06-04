"""
Inserts metereological data inside the recinto geojson file.
Author: Sebastian Pasker
"""

import json
import statistics
from config_python import ConfigPath
from geojson import FeatureCollection

data_path = ConfigPath.data_path()
file_recinto = "recintos_buffer_center.geojson"
file_nearest_point = "nearest_coords_by_coords_search.geojson"
file_output = "recintos_with_data.geojson"

data_recinto = None
with open(data_path + file_recinto, "r") as f:
    data_recinto = json.load(f)

with open(data_path + file_nearest_point, "r") as f:
    data_nearest_point = json.load(f)

# Buscamos el punto intermedio de las coordenadas del recinto
for feature in data_recinto["features"]:
    list_of_coordinates = feature["geometry"]["coordinates"][0]
    # Average of list of coordinates
    avg_x = statistics.mean([coord[0] for coord in list_of_coordinates])
    avg_y = statistics.mean([coord[1] for coord in list_of_coordinates])
    feature["properties"]["avg_coord"] = [avg_x, avg_y]

# Ordenamos los datos
data_recinto["features"] = sorted(
    data_recinto["features"], key=lambda x: x["properties"]["avg_coord"]
)

# Quitamos los 2 mas bajos (quitar) TODO
data_nearest_point["features"] = sorted(
    data_nearest_point["features"],
    key=lambda x: x["geometry"]["coordinates"][1],
)
data_recinto["features"] = data_recinto["features"][2:]

# Ordenadomos los datos de los puntos mas cercanos
data_nearest_point["features"] = sorted(
    data_nearest_point["features"],
    key=lambda x: x["geometry"]["coordinates"],
)

for i in range(0, len(data_recinto["features"])):
    data_recinto["features"][i]["properties"][
        "time"
    ] = data_nearest_point["features"][i]["properties"]["time"]
    data_recinto["features"][i]["properties"][
        "wave_height"
    ] = data_nearest_point["features"][i]["properties"]["wave_height"]

fc = FeatureCollection(data_recinto["features"])
with open(data_path + file_output, "w") as f:
    json.dump(fc, f)
