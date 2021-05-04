import os
import json
import math
from datetime import datetime



# taken from https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def listdirs(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

# inspired by https://github.com/mapbox/vector-tile-js/blob/master/lib/vectortilefeature.js#L129
def vectorToCoords(x, y, z, px, py):
    size = MVT_EXTENT * math.pow(2, z)
    x0 = MVT_EXTENT * x
    y0 = MVT_EXTENT * y
    def project(px, py):
        y2 = 180 - (y0-py) * 360 / size
        return (px + x0) * 360 / size - 180, 360 / math.pi * math.atan(math.exp(y2 * math.pi / 180)) - 90

    return project(px, py)


if __name__ == '__main__':

    level = 15

    MVT_EXTENT = 4096
    # Name of the feature you want to extract; e.g. Gebaeudeflaeche, Adresse
    FEATURE = "Gebaeudeflaeche"

    # open file to write the result
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    save_to = open(f'{FEATURE}-{timestamp}.geojsonl', 'w')

    DEBUG = False

    geoms = []

    for x in listdirs(f"{level}/"):
        for file_name in os.listdir(f"{level}/{x}/"):
            y = file_name.split(".")[0]

            if DEBUG:
                print("Tile")
                print([num2deg(int(x),int(y),int(level))[1], num2deg(int(x),int(y),int(level))[0]])
                print([num2deg(int(x),int(y)+1,int(level))[1], num2deg(int(x),int(y)+1,int(level))[0]])
                print([num2deg(int(x)+1,int(y),int(level))[1], num2deg(int(x)+1,int(y),int(level))[0]])
                print([num2deg(int(x)+1,int(y)+1,int(level))[1], num2deg(int(x)+1,int(y)+1,int(level))[0]])
                print([num2deg(int(x),int(y),int(level))[1], num2deg(int(x),int(y),int(level))[0]])

            bottom_left = num2deg(int(x)+1,int(y)+1,int(level))
            top_right = num2deg(int(x),int(y),int(level))
            x_span = top_right[0] - bottom_left[0]
            y_span = top_right[1] - bottom_left[1]
            if DEBUG:
                print(f"{level}/{x}/{y} = {top_right} ({bottom_left})")
                print(f"{x_span} / {y_span}")

            data = json.load(open(f"{level}/{x}/{file_name}"))
            if FEATURE in data:
                for i in data[FEATURE]["features"]:
                    if i["geometry"]["type"] == "Point":
                        coords = vectorToCoords(int(x),int(y) +1,level,i["geometry"]["coordinates"][0], i["geometry"]["coordinates"][1])
                        i["geometry"]["coordinates"] = coords
                    elif i["geometry"]["type"] == "Polygon":
                        for e_num, e_obj in enumerate(i["geometry"]["coordinates"]):
                            for c_num, c_obj in enumerate(e_obj):
                                coords = vectorToCoords(int(x), int(y) + 1, level, c_obj[0], c_obj[1])
                                i["geometry"]["coordinates"][e_num][c_num] = coords
                            i["geometry"]["coordinates"][e_num].append(i["geometry"]["coordinates"][e_num][0])
                    i["type"] = "Feature"
                    del i["id"]
                    save_to.write(json.dumps(i)+"\n")