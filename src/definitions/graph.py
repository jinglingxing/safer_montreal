from plotable import Plotable
from crime import Crime
from node import Node, GridNode, Coordinates
import copy as cp


class Graph (Plotable):

    def __init__(self):
        self._nodes = dict()
        self._node_int_to_id = dict()

    def get_nodes(self):
        return cp.copy(self._nodes)

    def get_node(self, index: int = None, id : str = None) -> Node:
        if index:
            return self._nodes[self._node_int_to_id[[index]]]
        if id:
            return self._nodes[id]

    def add_node(self, lat: float, lon: float):
        node = Node(lat, lon)
        self._nodes[node.id] = node

    def get_node_int_map(self):
        if not self._node_int_to_id:
            for index, key in enumerate(self._nodes):
                self._node_int_to_id[index+1] = key
        return cp.copy(self._node_int_to_id)
    
    def add_neighbour(self, node: Node, neighbour: Node):
        node.add_neighbour(neighbour.id)
        neighbour.add_neighbour(node.id)

    def get_neighbours(self, node: Node):
        return node.get_neighbours()


class GridGraph (Graph):

    def __init__(self, resolution: float = None, minima: Coordinates = None, extrema: Coordinates = None, json: dict = None):
        super().__init__()
        if json:
            self.resolution = json['resolution']
            for element in json['nodes']:
                self._nodes[element['id']] = Node(element['lat'], element['lon'],
                element['id'], element['crimes'], element['neighbours'])
            return
        self.resolution = resolution

        # add node in grid graph
        y_min, x_min = extrema
        y_max, x_max = minima
        y_minimal = y_min

        while x_max > x_min:
            lat = x_min + resolution / 2
            x_min += resolution
            while y_max > y_min:
                # add centered node in each 0.002*0.002 small grid
                lon = y_min + resolution / 2
                self.add_node(lat, lon)
                y_min += resolution
            y_min = y_minimal

    def add_node(self, lat: float, lon: float):
        node = GridNode(lat, lon)
        self._nodes[node.id] = node

    def find_and_add_neighbours(self, node: GridNode):
        """ check distances and make as neighbour if distance < resolution """
        for cur_node in self._nodes.values():
            if node.distance(cur_node) <= self.resolution + 0.00001:
                self.add_neighbour(node, cur_node)

    def create_edges(self):
        """ go over all the nodes """
        for node in self._nodes.values():
            self.find_and_add_neighbours(node)
        
    def add_crime_occurrence(self, crime: Crime):
        for node in self._nodes.values():
            node_zone = node.in_surrounding_zone(self.resolution, crime.lat, crime.lon)
            if node_zone:
                node.add_crime_occurrence(crime)
                break  # A crime belongs to only one Grid

    def plot(self, ax, color=None):
        for node in self._nodes.values():
            # node.node_plot(ax, color='b')
            if len(node.crimes) >= 5:
                node.node_plot(ax, color='r')
            else:
                node.node_plot(ax, color='g')

    def dict_representation(self):
        return {
                "resolution": self.resolution,
                "nodes": [node.dict_representation() for node in self._nodes.values()]
            }
            