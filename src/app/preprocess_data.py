import pandas as pd
import sys
sys.path.append('../')
sys.path.append('../definitions/')
sys.path.append('../features/')
import src.features.node_data
from src.features.preprocessing_graph import load_or_process_graph

if __name__ == "__main__":
    print(" running code ... ")

    # input_data_path = '../../data/node_data.csv'
    # grid_graph = load_or_process_graph('../../data/preprocessed_graph_test.json')
    # node_data.generate_node_data(grid_graph, '../../data/node_data.csv')
    # data = pd.read_csv(input_data_path, sep=',', encoding='latin-1', index_col=[0])




