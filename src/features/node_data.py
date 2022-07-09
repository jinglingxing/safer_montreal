import random
import pandas as pd
import os.path
from typing import List, Dict


def generate_node_data(grid_graph, file_path):
    """
    Create all the input data without crimes and save it in a CSV file
    :param grid_graph: the grid graph includes all the nodes representing the center of regions
    :return: None
    """
    if not os.path.exists(file_path):
        zones = list(grid_graph._zones.values())
        # geo = list(grid_graph.get_grid_node_coordinates_to_id().keys())
        time_of_day = ['jour', 'soir', 'nuit']
        time_of_day_to_int = {'jour': 1, 'soir': 2, 'nuit': 3}
        month_of_year = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        counter = 0
        node_dict = {}

        for zone in zones:
            n = random.randint(20, 24)
            for _ in range(n):
                time = time_of_day_to_int[random.choice(time_of_day)]
                month = random.choice(month_of_year)
                x, y = zone.x, zone.y
                node_dict[counter] = [time, month, x, y, zone.num_police_station, zone.num_fire_station]
                counter += 1
                print(counter)

        node_df = pd.DataFrame.from_dict(node_dict, orient='index',
                                         columns=['time_of_day', 'month_of_year', 'x', 'y',
                                                  'number of police station', 'number of fire station'])
        node_df = node_df.sample(frac=1).reset_index(drop=True)
        with open(file_path, 'w') as file:
            file.write(node_df.to_csv(line_terminator='\n'))


def add_feature(zone_json: Dict, feature: List[Dict], feature_name: str):
    """
    add more features to our zone(grid node)
    :param zone_json: preprocessed_grid_graph
    :param feature: new feature json file
    """
    resolution = zone_json["resolution"]
    new_feature_dict = {}
    grid_nodes = zone_json['grid_nodes']
    for grid_node in grid_nodes:
        x, y = grid_node['x'], grid_node['y']
        new_feature_dict[(x, y)] = 0

        for elem in feature:
            lon, lat = elem['geometry']['coordinates']
            if abs(grid_node['lat'] - lat) <= resolution/2 and abs(grid_node['lon'] - lon) <= resolution/2:
                new_feature_dict[(x, y)] += 1

    l = [[x, y, v] for (x, y), v in new_feature_dict.items()]
    return pd.DataFrame(l, columns=['x', 'y', feature_name])


if __name__ == '__main__':
    #from src.models.preprocessing_graph import load_or_process_graph
    #graph = load_or_process_graph('../../data/preprocessed_grid_graph.json')
    # generate_node_data(graph, '../../data/zone_data.csv')
    pass

