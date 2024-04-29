import json
from geojson import Feature, FeatureCollection

coords_str = []

# Sacar coordenada por linea de archivo
with open("points_by_recinto.txt", "r") as file:
    for line in file:
        if line.strip() != "":
            coords_str.append(line[:-2])

# Pasar a tupla de coordenadas
coords_search = []
for coord_s in coords_str:
    coords_search.append(list(map(float, coord_s.split(","))))

# Leemos en base a todos los puntos mas cercanos
with open("data.geojson", "r") as file:
    data = json.load(file)

# Guardamos solo las coordenadas.
data_coords = [
    data["features"][i]["geometry"]["coordinates"]
    for i in range(len(data["features"]))
]

features = []
for coord in coords_search:
    nearest_coord = [None, None]
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
    features.append(
        Feature(
            geometry={"type": "Point", "coordinates": nearest_coord}
        )
    )


# Buscamos los puntos mas cercanos
fc = FeatureCollection(features)

with open("nearest_coords_by_coords_search.geojson", "w") as file:
    json.dump(fc, file)
