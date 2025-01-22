import geojson
from config_python import ConfigPath

data_path = ConfigPath.data_path()
file_in = "recintos_buffer_center.geojson"
file_out = "recintos_buffer_center_with_img.geojson"

with open(data_path + file_in, "r") as f:
    data = geojson.load(f)

sorted_data = sorted(
    data["features"], key=lambda x: float(x["properties"]["center"][0])
)

piscifactoria_en = [
    "San Juan de los Terreros",
    "Aguilas",
    "Cartagena",
    "San Pedro del Pinatar",
    "Santa Pola",
    "El Campello",
    "Villajoyosa",
    "Sagunto",
    "Burriana",
    "Altea",
    "Burriana 2",
    "Calpe",
]

for i in range(len(sorted_data)):
    sorted_data[i]["properties"]["piscifactoria"] = piscifactoria_en[i]
    sorted_data[i]["properties"]["img"] = (
        piscifactoria_en[i].replace(" ", "_") + ".jpg"
    )

features = geojson.FeatureCollection(sorted_data)

with open(data_path + file_out, "w") as f:
    geojson.dump(features, f)
