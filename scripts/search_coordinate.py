import json

# Leo el archivo de entrada
with open("data.geojson") as f:
    data = json.load(f)

search_x = -1.290
search_y = 38.77

# Voy recorriendo cada valor por coordenada
for feature in data["features"]:
    # Creo un objeto Point con las coordenadas
    coord = feature["geometry"]["coordinates"]
    x = coord[0]
    y = coord[1]
    if abs(x - search_x) < 0.01:
        # if abs(y - search_y) < 0.01:
        print("Encontrado!")
        print(
            x,
            y,
            search_x,
            search_y,
            abs(x - search_x),
            abs(y - search_y),
        )
