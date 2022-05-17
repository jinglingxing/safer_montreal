import pandas as pd
from datetime import datetime
import sys
sys.path.append('../')
sys.path.append('../definitions/')
import graph
from crime import Crime
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print(" running code ... ")
    # import and process data
    crime_df = pd.read_csv('../../data/interventionscitoyendo.csv', sep=',', encoding='latin-1')
    crime_df = crime_df[:2000]

    crime_data = crime_df[crime_df['LATITUDE'] != 0]
    date_data = [datetime.strptime(crime_data.iloc[i]['DATE'], '%Y-%m-%d') for i in range(len(crime_data))]
    crime_year = [date_data[i].year for i in range(len(date_data))]
    crime_month = [date_data[i].month for i in range(len(date_data))]
    crime_data = crime_data.assign(CRIME_YEAR=crime_year)
    crime_data = crime_data.assign(CRIME_MONTH=crime_month)

    # find extrema
    extrema = (crime_data['LONGITUDE'].min(), crime_data['LATITUDE'].min())
    minima = (crime_data['LONGITUDE'].max(), crime_data['LATITUDE'].max())

    # build grid
    x_min = extrema[1]  # latitude
    y_min = extrema[0]  # longitude
    x_max = minima[1]  # latitude
    y_max = minima[0]  # longitude

    print('x_max', x_max,
          'y_max', y_max,
          'x_min', x_min,
          'y_min', y_min)

    resolution = 0.02
    grid_graph = graph.GridGraph(resolution=resolution, minima=minima, extrema=extrema)

    # add node in grid graph
    y_minimal = y_min

    while x_max > x_min:
        lat = x_min + resolution / 2
        x_min += resolution
        while y_max > y_min:
            # add centered node in each 0.002*0.002 small grid
            lon = y_min + resolution / 2
            grid_graph.add_node(lat, lon)
            y_min += resolution
        y_min = y_minimal

    # ingestion of crimes into our Nodes object
    for i in range(len(crime_data)):
        crime = Crime(crime_data.iloc[i]['LONGITUDE'], crime_data.iloc[i]['LATITUDE'],
                      crime_data.iloc[i]['CATEGORIE'], crime_data.iloc[i]['QUART'],
                      crime_data.iloc[i]['CRIME_MONTH'], crime_data.iloc[i]['CRIME_YEAR'])
        grid_graph.add_crime_occurrence(crime)

    # create edges
    grid_graph.create_edges()

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.autoscale(True)
    grid_graph.plot(ax)
    plt.show()




