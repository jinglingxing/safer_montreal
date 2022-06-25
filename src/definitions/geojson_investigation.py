import json

if __name__ == '__main__':
    cross_roads = json.load(open('../../data/geojson_cross_roads.json', 'r'))['features']
    roads = json.load(open('../../data/geojson_roads.json', 'r'))['features']

    xrn = set()
    rn = set()
    rn2 = list()

    for x in cross_roads:
        lon, lat = x['geometry']['coordinates']
        xrn.add((lon, lat))

    for r in roads:
        for lat, lon in r['geometry']['coordinates']:
            rn.add((lon, lat))
            rn2.append((lon, lat))

    print(len(xrn))
    print(len(rn), len(rn2))

    # print('coordinates not on roads (', len(xrn - rn))#, ') ', xrn - rn)
    # print('coordinates not in nodes (', len(rn - xrn), ') ', rn - xrn)
