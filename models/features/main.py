import random
import os.path
import pandas as pd
from datetime import datetime
import sys
sys.path.append('../')
sys.path.append('../definitions/')
import graph
import node_data
from crime import Crime
import matplotlib.pyplot as plt
from preprocessing_graph import load_or_process_graph

if __name__ == "__main__":
    print(" running code ... ")

    if os.path.exists('../../data/node_data.csv'):
        data = pd.read_csv('../../data/node_data.csv', sep=',', encoding='latin-1', index_col=[0])
    else:
        node_data.generate_node_data(grid_graph)
        data = pd.read_csv('../../data/node_data.csv', sep=',', encoding='latin-1', index_col=[0])
    grid_graph = load_or_process_graph()

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.autoscale(True)
    grid_graph.plot(ax)
    plt.show()




