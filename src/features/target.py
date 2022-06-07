import pandas as pd
import os


def filter_target(graph, path='../../data/target.csv'):
    if os.path.exists(path):
        pass
    else:
        df = pd.read_csv('../../data/node_data_test.csv', sep=',', encoding='latin-1')
        y = []
        for i in range(len(df)):
            probability = graph.filter(str(df.iloc[i]['node_number']), df.iloc[i]['time_of_day'],
                                       df.iloc[i]['month_of_year'])
            print(probability)
            y.append(probability)
        target = pd.DataFrame(y, columns=['target'])
        with open(path, 'w') as file:
            file.write(target.to_csv(line_terminator='\n'))


if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from preprocessing_graph import load_or_process_graph

    graph = load_or_process_graph(path='../../data/preprocessed_graph_test.json')
    print(filter_target(graph, path='../../data/target_test.csv'))



