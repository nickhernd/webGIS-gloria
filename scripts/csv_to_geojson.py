import sys
from geojson import Point, Feature, FeatureCollection, dump

if len(sys.argv) == 3:
    file_in = sys.argv[1]
    file_out = sys.argv[2]
else:
    file_in = "../data/coord_lonjas.csv"
    file_out = "../data/coord_lonjas.json"

with open(file_in, "r") as f:
    content = f.readlines()

f_collection = []
for line in content[1:]:
    data = line.split(",")
    f = Feature(
        geometry=Point((float(data[2]), float(data[1]))),
        properties={"Fish_market": data[0], "Color": "#ff7f50"},
    )
    f_collection.append(f)

with open(file_out, "w") as f:
    dump(FeatureCollection(f_collection), f)
