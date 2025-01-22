import csv
from geojson import Feature, FeatureCollection, Point
from config_python import ConfigPath
from tqdm import tqdm

# from threading import Thread, Lock

data_path = ConfigPath.data_path()
path_to_csv = data_path + "copernicus_data.csv"
path_to_geojson = data_path + "copernicus_data.geojson"

list_of_values = []

# CSV format is assumed to be: time,latitude,longitude,wave_height
# Guardamos los valores del csv en una lista de diccionarios
with open(path_to_csv, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")

    first = True
    for time, lat, lon, wave_height in reader:
        if first:
            first = False
            continue
        else:
            list_of_values.append(
                {
                    "coord": (float(lat), float(lon)),
                    "time": time,
                    "wave_height": wave_height,
                }
            )

# Sort the list of values by latitude and longitude
sorted_list = sorted(
    list_of_values, key=lambda x: (x["coord"][0], x["coord"][1])
)

coords = sorted(
    list(set([item["coord"] for item in list_of_values])),
    key=lambda x: (x[0], x[1]),
)


def obtain_time_and_wave_height(sorted_list, lat, lon):
    values_by_coord = list(
        filter(lambda x: x["coord"] == (lat, lon), sorted_list)
    )

    time_list = []
    wave_height_list = []

    es_tierra = False
    for value in values_by_coord:
        time_list.append(value["time"])
        wave_height_list.append(value["wave_height"])
        if value["wave_height"] == "":
            es_tierra = True
            break

    first_index = sorted_list.index(values_by_coord[0])
    last_index = sorted_list.index(values_by_coord[-1])

    return {
        "time": time_list if not es_tierra else None,
        "wave_height": wave_height_list if not es_tierra else None,
        "first_index": first_index,
        "last_index": last_index,
    }


features = []
used_coords = []
for coord, i in zip(coords, tqdm(range(len(coords)))):
    lat, lon = coord
    if coord in used_coords:
        continue
    else:
        time_and_wave_height = obtain_time_and_wave_height(
            sorted_list,
            lat,
            lon,
        )

        del sorted_list[
            time_and_wave_height["first_index"] : time_and_wave_height[
                "last_index"
            ]
            + 1
        ]

        if time_and_wave_height["wave_height"] is not None:
            f = Feature(
                geometry=Point((lon, lat)),
                properties={
                    "time": time_and_wave_height["time"],
                    "wave_height": time_and_wave_height["wave_height"],
                },
            )
            features.append(f)
        used_coords.append(coord)

collection = FeatureCollection(features)
with open(path_to_geojson, "w") as f:
    f.write("%s" % collection)
