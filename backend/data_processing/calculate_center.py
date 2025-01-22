from config_python import ConfigPath
import json
import statistics

data_path = ConfigPath.data_path()
file_in = "recintos_buffer.geojson"
file_out = "recintos_buffer_center.geojson"

with open(data_path + file_in, "r") as f:
    data = json.load(f)

for feature in data["features"]:
    center_x = statistics.mean(
        [point[0] for point in feature["geometry"]["coordinates"][0]]
    )
    center_y = statistics.mean(
        [point[1] for point in feature["geometry"]["coordinates"][0]]
    )
    feature["properties"]["center"] = [center_x, center_y]

with open(data_path + file_out, "w") as f:
    json.dump(data, f)
