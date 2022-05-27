
import random
import pandas as pd
import os.path

def generate_node_data(grid_graph, file_path):
    """
    Create all the input data without crimes and save it in a CSV file
    :param grid_graph: the grid graph includes all the nodes representing the center of regions
    :return: None
    """
    if not os.path.exists(file_path):
        geo = []
        time_of_day = ['day', 'night', 'evening']
        time_of_day_to_int = {'day': 1, 'evening': 2, 'night': 3}
        month_of_year = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        node_dict = {}

        for node in grid_graph.get_nodes().values():
            geo.append((node.lat, node.lon))

        for i in range(1000):
            lat, lon = random.choice(geo)
            time = time_of_day_to_int[random.choice(time_of_day)]
            month = random.choice(month_of_year)
            node_dict[i] = [time, month, lat, lon]

        node_df = pd.DataFrame.from_dict(node_dict, orient='index',
                                         columns=['time_of_day', 'month_of_year', 'latitude', 'longitude'])
        with open(file_path, 'w') as file:
            file.write(node_df.to_csv())



