import pandas as pd
import sys
sys.path.append('../')
sys.path.append('../definitions/')
sys.path.append('../features/')
import node_data
from preprocessing_graph import load_or_process_graph

if __name__ == "__main__":
    print(" running code ... ")

    input_data_path = '../../data/node_data.csv'
    grid_graph = load_or_process_graph('../../data/preprocessed_graph_test.json')
    node_data.generate_node_data(grid_graph, '../../data/node_data.csv')
    data = pd.read_csv(input_data_path, sep=',', encoding='latin-1', index_col=[0])


    # fig = plt.figure()
    # ax = fig.add_subplot()
    # ax.autoscale(True)
    # grid_graph.plot(ax)
    # plt.show()




