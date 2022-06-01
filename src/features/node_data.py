
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
        geo = list(grid_graph.get_node_int_map().keys())
        time_of_day = ['jour', 'soir', 'nuit']
        time_of_day_to_int = {'jour': 1, 'soir': 2, 'nuit': 3}
        month_of_year = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        node_dict = {}

        for i in range(300000):
            node_number = random.choice(geo)
            time = time_of_day_to_int[random.choice(time_of_day)]
            month = random.choice(month_of_year)
            node_dict[i] = [time, month, node_number]

        node_df = pd.DataFrame.from_dict(node_dict, orient='index',
                                         columns=['time_of_day', 'month_of_year', 'node_number'])
        with open(file_path, 'w') as file:
            file.write(node_df.to_csv(line_terminator='\n'))



