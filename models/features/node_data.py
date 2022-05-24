
import random
import pandas as pd


def generate_node_data(grid_graph):
    """
    Create all the input data without crimes and save it in a CSV file
    :param grid_graph: the grid graph includes all the nodes representing the center of regions
    :return: None
    """
    geo = []
    time_of_day = ['day', 'night', 'evening']
    month_of_year = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    node_dict = {}

    for node in grid_graph.get_nodes().values():
        geo.append((node.lat, node.lon))

    for i in range(1000):
        lat, lon = random.choice(geo)
        time = random.choice(time_of_day)
        month = random.choice(month_of_year)
        node_dict[i] = [time, month, lat, lon]

    node_df = pd.DataFrame.from_dict(node_dict, orient='index',
                                     columns=['time_of_day', 'month_of_year', 'latitude', 'longitude'])
    with open('../../data/node_data.csv', 'w') as file:
        file.write(node_df.to_csv())



