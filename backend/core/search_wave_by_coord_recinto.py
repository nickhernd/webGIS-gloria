import json
import sys
from config_python import ConfigPath
from geojson import Feature, FeatureCollection

coords_str = []

data_path = ConfigPath.data_path()

if len(sys.argv) == 2:
    data_file = sys.argv[1]
elif len(sys.argv) >= 3 and sys.argv[1] == "date":
    data_file = "data_by_date/data-" + sys.argv[2] + ".geojson"
else:
    data_file = "copernicus_data.geojson"

# Sacar coordenada por linea de archivo
with open(data_path + "points_by_recinto.txt", "r") as file:
    for line in file:
        if line.strip() != "":
            coords_str.append(line[:-2])

# Pasar a tupla de coordenadas
coords_search = []
for coord_s in coords_str:
    coords_search.append(list(map(float, coord_s.split(","))))

# Leemos en base a todos los puntos
with open(data_path + data_file, "r") as file:
    data = json.load(file)

# Guardamos solo las coordenadas.
data_coords = [
    data["features"][i]["geometry"]["coordinates"]
    for i in range(len(data["features"]))
]

features = []
# Buscamos las coordenadas mas cercanas al punto de las lonjas
for coord in coords_search:
    nearest_coord = [None, None]
    # Buscamos el punto mas cercano
    for data_coord in data_coords:
        if nearest_coord[0] is None:
            nearest_coord = data_coord
        else:
            if abs(data_coord[0] - coord[0]) + abs(
                data_coord[1] - coord[1]
            ) < abs(nearest_coord[0] - coord[0]) + abs(
                nearest_coord[1] - coord[1]
            ):
                nearest_coord = data_coord
    # Guardamos el indice
    index = data_coords.index(nearest_coord)

    # Guardamos en una lista de features
    features.append(
        Feature(
            geometry={"type": "Point", "coordinates": nearest_coord},
            properties=data["features"][index]["properties"],
        )
    )


# Guardamos en un feature collection
fc = FeatureCollection(features)

with open(
    data_path + "nearest_coords_by_coords_search.geojson", "w"
) as file:
    json.dump(fc, file)
