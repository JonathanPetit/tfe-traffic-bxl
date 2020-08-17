import json
from pyproj import Transformer

def lambertToWgs84(x, y):
    transformer = Transformer.from_crs("EPSG:31370", "EPSG:4326")
    lat, lng = transformer.transform(float(x), float(y))
    return lat, lng

output = {}

with open("quartierWGS.json") as f, open("quatierWGS.json", "w") as out:
    data = json.load(f)
    output["type"] = data["type"]
    output["name"] = data["name"]

    f = []
    count = 0
    for d in data["features"]:
        q = {}
        q["type"] = d["type"]
        q["properties"] = d["properties"]
        g = {}
        g["type"] = d["geometry"]["type"]
        coordinates = []


        if d["geometry"]["type"] == "MultiPolygon":
            continue

        for x in d["geometry"]["coordinates"]:
            for coord in x:
                coordinates.append([coord[1], coord[0]])
        
        g["coordinates"] = [coordinates]
        q["geometry"] = g
        f.append(q)
        count += 1
        print(count)

    output["features"] = f
    json.dump(output, out)

"""
with open("quartier.geojson") as f, open("quatierWGS.json", "w") as out:
    data = json.load(f)
    output["type"] = data["type"]
    output["name"] = data["name"]

    f = []
    count = 0
    for d in data["features"]:
        q = {}
        q["type"] = d["type"]
        q["properties"] = d["properties"]
        g = {}
        g["type"] = d["geometry"]["type"]
        coordinates = []
 
        c_lat = 100
        c_lng = 100
        c_lat1 = 0
        c_lng1 = 0

        if d["geometry"]["type"] == "MultiPolygon":
            continue

        for x in d["geometry"]["coordinates"]:
            for coord in x:
                lat, lng = lambertToWgs84(coord[0], coord[1])
                if lat < c_lat:
                    c_lat = lat
                if lng < c_lng:
                    c_lng = lng
                if lat > c_lat1:
                    c_lat1 = lat
                if lng > c_lng1:
                    c_lng1 = lng
                coordinates.append([lat, lng])

        latitude = c_lat + ((c_lat1 - c_lat) / 2);
        longitude = c_lng + ((c_lng1 - c_lng) / 2);
        
        g["coordinates"] = [coordinates]
        q["geometry"] = g
        f.append(q)
        count += 1
        print(count)

    output["features"] = f
    json.dump(output, out)
"""

