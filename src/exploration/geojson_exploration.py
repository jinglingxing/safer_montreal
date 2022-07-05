def is_in_nodes(nodes, lat, lon):
    for elem in nodes['features']:
        if elem['geometry']['coordinates'] == [lon, lat]:
            return True
    return False

def min_distance(nodes, lat, lon):
    min_dist = 100000
    min_lat = 0
    min_lon = 0
    for elem in nodes['features']:
        lon_n, lat_n = elem['geometry']['coordinates']
        d = abs(lat - lat_n) + abs(lon - lon_n)
        if d < min_dist:
            min_dist = d
            min_lat = lat_n
            min_lon = lon_n
    return f"{min_dist}, {min_lat}, {min_lon}, {lat}, {lon}"

if __name__ == "__main__":
    import json
    import pandas as pd
    with open('../../data/noeud.json') as f:
        nodes = json.load(f)
    
    crime_df = pd.read_csv('../../data/interventionscitoyendo.csv', sep=',', encoding='latin-1')
    crime_df = crime_df[:2000]

    crime_data = crime_df[crime_df['LATITUDE'] != 0]
    all_true = True
    for i in range(len(crime_data)):
        res = min_distance(nodes, crime_data.iloc[i]['LATITUDE'], crime_data.iloc[i]['LONGITUDE'])
        print(res)