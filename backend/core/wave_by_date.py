import json
from config_python import ConfigPath
from datetime import datetime
from geojson import Feature, FeatureCollection

data_path = ConfigPath.data_path()


def compare_year_month_day(datetime1, datetime2):
    if datetime1.year == datetime2.year:
        if datetime1.month == datetime2.month:
            if datetime1.day == datetime2.day:
                return True
    return False


# Leemos de la base de datos
with open(data_path + "data.geojson") as f:
    data = json.load(f)

date_str = "2024-04-23"

# date_search = datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
date_search = datetime.strptime(date_str, "%Y-%m-%d")

indexes = []
# Buscamos en la base de datos el indice de la fecha
index = 0
for date_feature in data["features"][0]["properties"]["time"]:
    if compare_year_month_day(
        date_search,
        datetime.strptime(date_feature, "%Y-%m-%d %H:%M:%S"),
    ):
        indexes.append(index)
    index += 1

features_search = []
for feature in data["features"]:
    f = Feature(
        geometry=feature["geometry"],
        properties={
            "time": [feature["properties"]["time"][i] for i in indexes],
            "wave_height": [
                feature["properties"]["wave_height"][i] for i in indexes
            ],
        },
    )
    features_search.append(f)

# Escribimos en un nuevo archivo
feature_collection = FeatureCollection(features_search)
with open(data_path + "data_search.geojson", "w") as f:
    json.dump(feature_collection, f)
