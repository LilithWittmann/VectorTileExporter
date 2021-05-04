import math
import mapbox_vector_tile
import requests
import json
import os

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)


def save_result(filename, content):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as f:
        f.write(content)


if __name__ == "__main__":

    # e.g. https://adv-smart.de/tiles/smarttiles_de_public_v1/
    URL = ""

    LEVEL = 15
    #convert to top right and bottom left
    tr = deg2num(47.23,5.53, level)
    bl = deg2num(54.96,15.38, level)

    i = 0

    for x in range(tr[0], bl[0]):
        for y in range(bl[1], tr[1]):
            url = f"{URL}{LEVEL}/{x}/{y}.pbf"
            try:
                result = requests.get(url)
                geojson = mapbox_vector_tile.decode(result.content)
                if geojson:
                    save_result(f'{level}/{x}/{y}.json', json.dumps(geojson))
                i += 1
                if i % 100 == 0:
                    print(i)
            except Exception as e:
                print(e)