import pandas as pd
from datetime import datetime
import sys
sys.path.append('../')
sys.path.append('../definitions/')
import graph
sys.path.append('../features/')
import node_data
from crime import Crime
import matplotlib.pyplot as plt
from preprocessing_graph import load_or_process_graph

if __name__ == "__main__":
    print(" running code ... ")

    input_data_path = '../../data/node_data.csv'
    node_data.generate_node_data(grid_graph, input_data_path)
    data = pd.read_csv(input_data_path, sep=',', encoding='latin-1', index_col=[0])

    print(data)

    grid_graph = load_or_process_graph()

    # fig = plt.figure()
    # ax = fig.add_subplot()
    # ax.autoscale(True)
    # grid_graph.plot(ax)
    # plt.show()




