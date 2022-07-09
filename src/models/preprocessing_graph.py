import pandas as pd
from datetime import datetime
import sys
import os
sys.path.append('../')
sys.path.append('../definitions/')
import graph
import json


def load_or_process_graph(path='../../data/preprocessed_graph.json'):
    if os.path.exists(path):
        return graph.GridGraph(json=json.load(open(path, 'r')))
    else:
        return preprocess_graph(path)


def preprocess_graph(path = '../../data/preprocessed_graph.json'):
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

    cross_roads = json.load(open('../../data/geojson_cross_roads.json', 'r'))['features']
    roads = json.load(open('../../data/geojson_roads.json', 'r'))['features']

    grid_graph = graph.GridGraph(
        resolution=resolution,
        crime_data=crime_data,
        cross_roads=cross_roads,
        roads=roads
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


    gg = load_or_process_graph('../../data/preprocessed_grid_graph.json')
    print(len(gg._nodes), len(gg._grid_nodes))
    print('took: ', time.time() - st)
