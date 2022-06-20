import pandas as pd
import os
from threading import Thread
import numpy as np
from numba import jit


def filter_target(graph, path='../../data/target.csv'):
    if os.path.exists(path):
        pass
    else:
        df = pd.read_csv('../../data/node_data.csv', sep=',', encoding='latin-1')
        n_threads = 6
        l = [ list() for _ in range(n_threads)]
        threads = []
        for index, partdf in enumerate(np.array_split(df, n_threads)):
            t = Thread(target=filter, args=(index, partdf, graph, l[index]))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        y = list(np.concatenate(l))
        target = pd.DataFrame(y, columns=['target'])
        with open(path, 'w') as file:
            file.write(target.to_csv(line_terminator='\n'))


@jit
def filter(thread_index, df, graph, y):
    if thread_index == 0:
        print("the objective for this thread is to reach: ", len(df))
    for i in range(len(df)):
        if thread_index == 0:
            print(i)
        probability = graph.filter(str(df.iloc[i]['node_number']), df.iloc[i]['time_of_day'],
                                   df.iloc[i]['month_of_year'])
        # if thread_index == 0:
        #     print(probability)
        y.append(probability)


if __name__ == '__main__':
    import sys
    sys.path.append('../models')
    from preprocessing_graph import load_or_process_graph

    graph = load_or_process_graph(path='../../data/preprocessed_graph.json')
    filter_target(graph, path='../../data/target.csv')



