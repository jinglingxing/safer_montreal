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
        counter = 0
        node_dict = {}

        for node_number in geo:
            if node_number == geo[36]:
                n = random.randint(20, 24)
                for _ in range(1000):
                    time = time_of_day_to_int[random.choice(time_of_day)]
                    month = random.choice(month_of_year)
                    node_dict[counter] = [time, month, node_number]
                    counter += 1
                    print(counter)

        node_df = pd.DataFrame.from_dict(node_dict, orient='index',
                                         columns=['time_of_day', 'month_of_year', 'node_number'])
        node_df = node_df.sample(frac=1).reset_index(drop=True)
        with open(file_path, 'w') as file:
            file.write(node_df.to_csv(line_terminator='\n'))

if __name__ == '__main__':
    from src.models.preprocessing_graph import load_or_process_graph
    graph = load_or_process_graph('../../data/preprocessed_graph_test.json')
    generate_node_data(graph, '../../data/node_data_t.csv')

