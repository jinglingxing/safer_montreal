from plotable import Plotable
from crime import Crime
from node import Node, GridNode, Coordinates
import copy as cp
from typing import List, Dict


class Graph(Plotable):

    def __init__(self):
        self._nodes: Dict[str, Node] = dict()
        self._node_int_to_id: Dict[str, str] = dict()

    def get_nodes(self):
        return cp.copy(self._nodes)

    def get_node(self, index: str = None, id: str = None) -> Node:
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
                self._node_int_to_id[str(index + 1)] = key
        return cp.copy(self._node_int_to_id)

    def add_neighbour(self, node: Node, neighbour: Node):
        node.add_neighbour(neighbour.id)
        neighbour.add_neighbour(node.id)

    def get_neighbours(self, node: Node) -> List[str]:
        return node.get_neighbours()

    def find_closest_node(self, lat: float, lon: float) -> Node:
        nodes = list(self._nodes.values())
        closest_node = nodes[0]
        minimum_dist = closest_node.distance(lat, lon)
        for node in nodes[1::]:
            dist = node.distance(lat, lon)
            if dist < minimum_dist:
                minimum_dist = dist
                closest_node = node
        return closest_node

    def filter(self, node_number, time_of_day, month):
        reverse_map = {1: 'jour', 2: 'soir', 3: 'nuit'}
        time_of_day = reverse_map[time_of_day]
        num_crimes_list = []
        for node in self._nodes.values():
            num_crimes = node.filter(time_of_day, month)
            num_crimes_list.append(num_crimes)
        max_num_crimes = max(num_crimes_list)
        node_id = self._node_int_to_id(node_number)
        node = self._nodes[node_id]
        num_crimes = node.filter(time_of_day, month)
        probability = float(num_crimes)/max_num_crimes
        return probability


class GridGraph(Graph):

    def __init__(self, resolution: float = None, minima: Coordinates = None, extrema: Coordinates = None,
                 json: dict = None):
        super().__init__()
        if json:
            self.resolution = json['resolution']
            for element in json['nodes']:
                self._nodes[element['id']] = Node(element['lat'], element['lon'],
                                                  element['id'], element['crimes'], element['neighbours'])
            self._node_int_to_id = json['int_to_id']
            return
        self.resolution = resolution

        # add node in grid graph
        y_min, x_min = minima
        y_max, x_max = extrema
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
            if node.distance_node(cur_node) <= self.resolution + 0.00001:
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
            "int_to_id": self.get_node_int_map(),
            "nodes": [node.dict_representation() for node in self._nodes.values()]
        }


if __name__ == '__main__':
    import json

    with open('../../data/preprocessed_graph.json', 'r') as f:
        json_obj = json.load(f)
        g = GridGraph(json=json_obj)

    with open('../../data/preprocessed_graph.json', 'w') as f:
        f.write(json.dumps(json.loads(str(g.dict_representation()).replace("\'", "\"")), indent=4,
                           sort_keys=False))