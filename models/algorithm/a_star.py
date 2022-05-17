import sys
sys.path.append('../')
sys.path.append('../definitions/')
from node import Node
from typing import List

class AStar:
    def __init__(self, graph):
        self.graph = graph

    def find_path(self, start_node: Node, end_node: Node) -> List[Node]:
        
        pass

