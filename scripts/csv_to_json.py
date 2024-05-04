import csv
from geojson import Feature, FeatureCollection, Point
from config_python import ConfigPath

data_path = ConfigPath.data_path()
path_to_csv = data_path + "copernicus_data.csv"
path_to_geojson = data_path + "copernicus_data.geojson"


def save_until_coord(sorted_list, index, lon, lat):
    time_list = []
    wave_height_list = []
    while (
        index < len(sorted_list)
        and sorted_list[index]["lat"] == lat
        and sorted_list[index]["lon"] == lon
    ):
        time_list.append(sorted_list[index]["time"])
        wave_height_list.append(sorted_list[index]["wave_height"])
        index += 1
    return time_list, wave_height_list, index


list_of_values = []
# CSV format is assumed to be: time,latitude,longitude,wave_height
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

    for value in values_by_coord:
        time_list.append(value["time"])
        wave_height_list.append(value["wave_height"])
        if value["wave_height"] == "":
            return None

    return {
        "time": time_list,
        "wave_height": wave_height_list,
    }


features = []
used_coords = []
for coord in coords:
    lat, lon = coord
    if coord in used_coords:
        continue
    else:
        time_and_wave_height = obtain_time_and_wave_height(
            sorted_list, lat, lon
        )
        if time_and_wave_height is not None:
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
