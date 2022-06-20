import pandas as pd
from datetime import datetime
import sys
import os
sys.path.append('../')
sys.path.append('../definitions/')
import graph
from crime import Crime
import json


def load_or_process_graph(path='../../data/preprocessed_graph.json'):
    if os.path.exists(path):
        return graph.GridGraph(json=json.load(open(path, 'r')))
    else:
        return preprocess_graph(path)


def preprocess_graph(path = '../../data/preprocessed_graph.json'):
    crime_df = pd.read_csv('../../data/interventionscitoyendo.csv', sep=',', encoding='latin-1')
    #crime_df = crime_df[:2000]

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

     # find extrema
    minima = (crime_data['LONGITUDE'].min(), crime_data['LATITUDE'].min())
    extrema = (crime_data['LONGITUDE'].max(), crime_data['LATITUDE'].max())

    # build grid
    x_min = minima[1]  # latitude
    y_min = minima[0]  # longitude
    x_max = extrema[1]  # latitude
    y_max = extrema[0]  # longitude

    print('x_max', x_max,
          'y_max', y_max,
          'x_min', x_min,
          'y_min', y_min)

    resolution = 0.002
    grid_graph = graph.GridGraph(resolution=resolution, minima=minima, extrema=extrema)

    # ingestion of crimes into our Nodes object
    for i in range(len(crime_data)):
        crime = Crime(crime_data.iloc[i]['LATITUDE'], crime_data.iloc[i]['LONGITUDE'],
                      crime_data.iloc[i]['CATEGORIE'], crime_data.iloc[i]['QUART'],
                      crime_data.iloc[i]['CRIME_MONTH'], crime_data.iloc[i]['CRIME_YEAR'])
        grid_graph.add_crime_occurrence(crime)

    # create edges
    grid_graph.create_edges()

    with open(path, 'w') as file:
        file.write(json.dumps(json.loads(str(grid_graph.dict_representation()).replace("\'", "\"")), indent=4, sort_keys=False))

    return grid_graph


if __name__ == "__main__":
    print(" running code ... ")
    # import and process data
    preprocess_graph()

    