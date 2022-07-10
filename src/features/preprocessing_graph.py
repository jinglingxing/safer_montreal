import pandas as pd
from datetime import datetime
import os
import src.definitions.graph as graph
import json


def load_or_process_graph(path='../../data/preprocessed_grid_graph.json'):
    if os.path.exists(path):
        return graph.MapGraph(json=json.load(open(path, 'r')))
    else:
        return preprocess_graph(path)


def preprocess_graph(path = '../../data/preprocessed_grid_graph.json'):
    crime_df = pd.read_csv('../../data/interventionscitoyendo.csv', sep=',', encoding='latin-1')
    # crime_df = crime_df[:200]

    crime_data = crime_df[crime_df['LATITUDE'] != 0]
    date_data = [datetime.strptime(crime_data.iloc[i]['DATE'], '%Y-%m-%d') for i in range(len(crime_data))]
    crime_year = [date_data[i].year for i in range(len(date_data))]
    crime_month = [date_data[i].month for i in range(len(date_data))]
    crime_data = crime_data.assign(CRIME_YEAR=crime_year)
    crime_data = crime_data.assign(CRIME_MONTH=crime_month)
    crime_type_map = {"Introduction": 1,
                      "M\u00e9fait": 2,
                      "Vols qualifi\u00e9s": 3,
                      "Vol dans / sur v\u00e9hicule \u00e0 moteur": 4,
                      "Vol de v\u00e9hicule \u00e0 moteur": 5,
                      "Infractions entrainant la mort": 6}
    crime_data = crime_data.replace({"CATEGORIE": crime_type_map})

    resolution = 0.002

    roads = json.load(open('../../data/geojson_roads.json', 'r'))['features']
    police_station_json = json.load(open('../../data/police-station.json', 'r'))['features']
    fire_station_json = json.load(open('../../data/fire-station.json', 'r'))['features']

    grid_graph = graph.MapGraph(
        resolution=resolution,
        crime_data=crime_data,
        roads=roads,
        police_station_json=police_station_json,
        fire_station_json=fire_station_json
    )

    with open(path, 'w') as file:
        s = str(grid_graph.dict_representation()).replace("\'", "\"")
        # print(s)
        j = json.loads(s)
        # print(j)
        file.write(json.dumps(j, indent=4, sort_keys=False))

    return grid_graph


if __name__ == "__main__":
    import time
    print(" running code ... ")
    st = time.time()
    # import and process data
    # preprocess_graph('../../data/preprocessed_grid_graph.json')


    gg = load_or_process_graph('../../model/preprocessed_map_graph.json')
    # gg.process_station(json.load(open('../../data/police-station.json', 'r'))['features'], "police_stations")
    # gg.process_station(json.load(open('../../data/fire-station.json', 'r'))['features'], "fire_stations")
    # with open('../../data/preprocessed_map_graph.json', 'w') as file:
    #     s = str(gg.dict_representation()).replace("\'", "\"")
    #     # print(s)
    #     j = json.loads(s)
    #     # print(j)
    #     file.write(json.dumps(j, indent=4, sort_keys=False))
    print('took: ', time.time() - st)
