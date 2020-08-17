import csv
from pyproj import Transformer

def lambertToWgs84(x, y):
    transformer = Transformer.from_crs("EPSG:31370", "EPSG:4326")
    x = x.replace(",", ".")
    y = y.replace(",", ".")
    lat, lng = transformer.transform(float(x), float(y))
    return lat, lng

fieldnames = ["region", "province", "arrondissement", "commune", "secteur_statistique", "latitude", "longitude"]
with open("TU_GEO_LPW_CODES.csv", "r") as inp, open("output-cities-latlong.csv", "w") as out:
    reader = csv.DictReader(inp, delimiter=',')
    writer = csv.DictWriter(out, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        pass

if __name__ == "__main__":
    pass
