import json
from config_python import ConfigPath
from datetime import datetime
from geojson import Feature, Point, FeatureCollection

data_path = ConfigPath.data_path()
file_in = data_path + "copernicus_data.geojson"

with open(file_in, "r") as f:
    data = json.load(f)

date_dict = {}
# Obtenemos el rango de fechas
date_list = data["features"][0]["properties"]["time"]
index = 0
last_date = None
for str_date in date_list:
    date = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    if date.strftime("%Y-%m-%d") not in date_dict:
        date_dict[date.strftime("%Y-%m-%d")] = None

    # Primer caso
    if last_date is None:
        last_date = date
        date_dict[date.strftime("%Y-%m-%d")] = {"range": [index, None]}

    # Caso que la fecha sea diferente
    if date.strftime("%Y-%m-%d") != last_date.strftime("%Y-%m-%d"):
        date_dict[last_date.strftime("%Y-%m-%d")]["range"][1] = (
            index - 1
        )
        date_dict[date.strftime("%Y-%m-%d")] = {"range": [index, None]}
        last_date = date

    index += 1

# Ultimo caso
date_dict[last_date.strftime("%Y-%m-%d")]["range"][1] = index - 1

for key in date_dict:
    date_dict[key]["features"] = []
    for coord in data["features"]:
        date_dict[key]["features"].append(
            Feature(
                geometry=Point(coord["geometry"]["coordinates"]),
                properties={
                    "time": coord["properties"]["time"][
                        date_dict[key]["range"][0] : date_dict[key][
                            "range"
                        ][1]
                        + 1
                    ],
                    "wave_height": coord["properties"]["wave_height"][
                        date_dict[key]["range"][0] : date_dict[key][
                            "range"
                        ][1]
                        + 1
                    ],
                },
            )
        )

for key in date_dict:
    with open(
        data_path + "/data_by_date/data-" + key + ".geojson", "w"
    ) as f:
        json.dump(FeatureCollection(date_dict[key]["features"]), f)
