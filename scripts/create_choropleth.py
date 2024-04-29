from geojson import Feature, FeatureCollection, Polygon
import json

read_data = "nearest_coords_by_coords_search.geojson"
# Abrimos los datos
with open(read_data) as f:
    data = json.load(f)

tam_cuadrado = 0.041666 / 2
esquina_superior_izq = [-tam_cuadrado, tam_cuadrado]
esquina_inferior_izq = [-tam_cuadrado, -tam_cuadrado]
esquina_superior_der = [tam_cuadrado, tam_cuadrado]
esquina_inferior_der = [tam_cuadrado, -tam_cuadrado]

features = []

# Creamos un polygono en base a los puntos
for feature in data["features"]:
    coords = feature["geometry"]["coordinates"]
    # Creamos un cuadrado
    new_feature = Feature(
        geometry=Polygon(
            [
                [
                    (
                        coords[0] + esquina_superior_izq[0],
                        coords[1] + esquina_superior_izq[1],
                    ),
                    (
                        coords[0] + esquina_inferior_izq[0],
                        coords[1] + esquina_inferior_izq[1],
                    ),
                    (
                        coords[0] + esquina_inferior_der[0],
                        coords[1] + esquina_inferior_der[1],
                    ),
                    (
                        coords[0] + esquina_superior_der[0],
                        coords[1] + esquina_superior_der[1],
                    ),
                ]
            ]
        )
    )

    features.append(new_feature)


# Escribimos en otro archivo
collection = FeatureCollection(features)
with open("data_choropleth.geojson", "w") as f:
    f.write(json.dumps(collection))
