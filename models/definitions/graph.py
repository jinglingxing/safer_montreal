from plotable import Plotable
from crime import Crime
from node import Node, GridNode, Coordinates
import copy as cp


class Graph (Plotable):

    def __init__(self):
        self._nodes = dict()

    def get_nodes(self):
        return cp.copy(self._nodes)

    def add_node(self, lat: float, lon: float):
        node = Node(lat, lon)
        self._nodes[node.id] = node
    
    def add_neighbour(self, node: Node, neighbour: Node):
        node.add_neighbour(neighbour)
        neighbour.add_neighbour(node)

    def get_neighbours(self, node: Node):
        return node.get_neighbours()   


class GridGraph (Graph):

    def __init__(self, resolution: float, minima: Coordinates, extrema: Coordinates):
        super().__init__()
        self.resolution = resolution

    def add_node(self, lat: float, lon: float):
        node = GridNode(lat, lon)
        self._nodes[node.id] = node

    def find_and_add_neighbours(self, node: GridNode):
        for _, cur_node in self._nodes:
            if node.distance(cur_node) == self.resolution:
                self.add_neighbour(node, cur_node)

    def create_edges(self):
        for _, node in self._nodes:
            self.find_and_add_neighbours(node)
        
    def add_crime_occurrence(self, crime: Crime):
        for _, node in self._nodes:
            if node.in_surrounding_zone(self.resolution, crime.lat, crime.long):
                node.add_crime_occurrence(crime)
                break # A crime belongs to only one Grid

    def plot(self, ax, color=None):
        for node in self._nodes.values():
            node.node_plot(ax, color='b')
