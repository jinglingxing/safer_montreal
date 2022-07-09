from src.definitions.crime import Crime
from src.definitions.node import Node, GridNode, Coordinates
import copy as cp
from typing import List, Dict, Tuple
from numba import jit
import pandas as pd


class Graph(object):

    def __init__(self):
        self._nodes: Dict[str, Node] = dict()

    def get_nodes(self):
        return cp.copy(self._nodes)

    def get_node(self, id: str) -> Node:
        return self._nodes[id]

    def add_node(self, lat: float, lon: float) -> Node:
        node = Node(lat, lon)
        self._nodes[node.id] = node
        return node

    def add_neighbour(self, node: Node, neighbour: Node):
        node.add_neighbour(neighbour.id)
        neighbour.add_neighbour(node.id)

    def get_neighbours(self, node: Node) -> List[str]:
        return node.get_neighbours()
    
    def find_node(self, lat: float, lon: float) -> Node:
        for node in self._nodes.values():
            if node.lat == lat and node.lon == lon:
                return node

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


class GridGraph(Graph):

    def __init__(self,
                 resolution: float = None,
                 crime_data: pd.DataFrame = None,
                 cross_roads: List[Dict] = None,
                 roads: List[Dict] = None,
                 json: dict = None):
        super().__init__()
        self._grid_nodes: Dict[str, GridNode] = dict()
        self._grid_node_coordinates_to_id: Dict[Tuple[int, int], str] = dict()

        # if we preprocessed the graph and saved it in json form, read it.
        if json:
            self.resolution = json['resolution']
            print('### processing nodes')
            total_nodes = len(json['nodes'])
            for index, element in enumerate(json['nodes']):
                print('processing node number ', index, 'over ', total_nodes)
                self._nodes[element['id']] = Node(element['lat'], element['lon'],
                                                  element['id'], element['grid_node_id'], element['neighbours'])
            print('### processing grid nodes')
            total_grid_nodes = len(json['grid_nodes'])
            for index, element in enumerate(json['grid_nodes']):
                print('processing grid node number ', index, 'over ', total_grid_nodes)
                self._grid_nodes[element['grid_node_id']] = GridNode(element['lat'], element['lon'],
                                                                     element['x'], element['y'],
                                                                     element['grid_node_id'], element['crimes'])
            self._grid_node_coordinates_to_id = {eval(k): v for k, v in json['grid_node_coordinates_to_id'].items()}
            return

        # normal initialization, with all the preprocessing
        self.resolution = resolution

        # add cross-roads
        # for element in cross_roads:
        #     lon, lat = element['geometry']['coordinates']
        #     node = self.add_node(lat, lon)
        #     inside_montreal.add(self.link_node_to_gridnode(node))
        #     print('added node ', node.id)

        # manage cross-roads and edges
        self.min_lat = self.min_lon = 10000
        self.max_lat = self.max_lon = -10000
        for element in roads:
            print('processing road ', element['properties']['NOM_VOIE'])
            coordinates = element['geometry']['coordinates']
            # nodes = [self.add_node(lat, lon) for lon, lat in coordinates]
            # for i in range(len(nodes)):
            #     inside_montreal.add(self.link_node_to_gridnode(nodes[i]))
            #     if i < len(nodes)-1:
            #         self.add_neighbour(nodes[i], nodes[i+1])
            lon_start, lat_start = coordinates[0]
            lon_end, lat_end = coordinates[-1]
            node_start = self.find_node(lat_start, lon_start)
            if node_start is None:
                node_start = self.add_node(lat_start, lon_start)
                self.check_extremum(lat_start, lon_start)

            node_end = self.find_node(lat_end, lon_end)
            if node_end is None:
                node_end = self.add_node(lat_end, lon_end)
                self.check_extremum(lat_end, lon_end)

            self.add_neighbour(node_start, node_end)


        # add node in grid graph
        x_min, y_min = self.min_lat, self.min_lon
        x_max, y_max = self.max_lat, self.max_lon
        y_minimal = y_min

        print('x_max', x_max,
              'y_max', y_max,
              'x_min', x_min,
              'y_min', y_min)

        counter_x = 0
        while x_max > x_min:
            counter_y = 0
            lat = x_min + resolution / 2
            x_min += resolution
            while y_max > y_min:
                # add centered node in each 0.002*0.002 small grid
                lon = y_min + resolution / 2
                grid_node = self.add_grid_node(lat, lon, counter_x, counter_y)
                self._grid_node_coordinates_to_id[(counter_x, counter_y)] = grid_node.id
                print('added grid node : ', grid_node.id)
                y_min += resolution
                counter_y += 1
            y_min = y_minimal
            counter_x += 1

        # ingestion of crimes into our GridNode objects
        for i in range(len(crime_data)):
            crime = Crime(crime_data.iloc[i]['LATITUDE'], crime_data.iloc[i]['LONGITUDE'],
                          crime_data.iloc[i]['CATEGORIE'], crime_data.iloc[i]['QUART'],
                          crime_data.iloc[i]['CRIME_MONTH'], crime_data.iloc[i]['CRIME_YEAR'])
            self.add_crime_occurrence(crime)
            print('ingested crime ', i, 'over ', len(crime_data))

        # find a corresponding grid_node to all the nodes
        inside_montreal = set()
        for node in self._nodes.values():
            print('finding corresponding grid_node to node ', node.id)
            try:
                inside_montreal.add(self.link_node_to_gridnode(node))
            except KeyError:
                print('ERROR:', node.lat, node.lon)
                raise KeyError

        # clean gridnodes outside montreal
        outside_montreal = self._grid_nodes.keys() - inside_montreal
        for _id in outside_montreal:
            print('removing node ', _id)
            if len(self._grid_nodes[_id].crimes):
                print(self._grid_nodes[_id].crimes)
                #raise ValueError
            grid_node = self._grid_nodes[_id]
            del self._grid_node_coordinates_to_id[(grid_node.x, grid_node.y)]
            del self._grid_nodes[_id]

    def check_extremum(self, lat, lon):
        if lat <= self.min_lat:
            self.min_lat = lat
        if lon <= self.min_lon:
            self.min_lon = lon
        if lat >= self.max_lat:
            self.max_lat = lat
        if lon >= self.max_lon:
            self.max_lon = lon

    def link_node_to_gridnode(self, node: Node) -> str:
        for grid_node in self._grid_nodes.values():
            node_zone = grid_node.in_surrounding_zone(self.resolution, node.lat, node.lon)
            if node_zone:
                node.grid_node_id = grid_node.id
                return grid_node.id
        raise KeyError

    def add_grid_node(self, lat: float, lon: float, x: int, y: int) -> GridNode:
        node = GridNode(lat, lon, x, y)
        self._grid_nodes[node.id] = node
        return node

    def get_grid_node_coordinates_to_id(self):
        return cp.copy(self._grid_node_coordinates_to_id)

    def add_crime_occurrence(self, crime: Crime):
        for grid_node in self._grid_nodes.values():
            node_zone = grid_node.in_surrounding_zone(self.resolution, crime.lat, crime.lon)
            if node_zone:
                grid_node.add_crime_occurrence(crime)
                break  # A crime belongs to only one Grid

    @jit
    def filter(self, x, y, time_of_day, month):
        reverse_map = {1: 'jour', 2: 'soir', 3: 'nuit'}
        time_of_day = reverse_map[time_of_day]
        node_id = self._grid_node_coordinates_to_id[(x, y)]
        grid_node = self._grid_nodes[node_id]
        node_prob_crimes = grid_node.filter(time_of_day, month)
        total_crimes = grid_node.total_crimes

        if not node_prob_crimes:
            return 0
        max = 0
        for grid_node in self._grid_nodes.values():
            crimes = grid_node.total_crimes
            if crimes > max:
                max = crimes
        probability = node_prob_crimes * float(total_crimes)/max if max else 0
        return probability

    def get_partial_input(self, node: Node):
        grid_node = self._grid_nodes[node.grid_node_id]
        return grid_node.x, grid_node.y, None, None

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
            "grid_node_coordinates_to_id": {str(k): v for k, v in self.get_grid_node_coordinates_to_id().items()},
            "nodes": [node.dict_representation() for node in self._nodes.values()],
            "grid_nodes": [grid_node.dict_representation() for grid_node in self._grid_nodes.values()]
        }


if __name__ == '__main__':
    # import json
    #
    # with open('../../data/preprocessed_graph.json', 'r') as f:
    #     json_obj = json.load(f)
    #     g = GridGraph(json=json_obj)
    #
    # with open('../../data/preprocessed_graph.json', 'w') as f:
    #     f.write(json.dumps(json.loads(str(g.dict_representation()).replace("\'", "\"")), indent=4,
    #                        sort_keys=False))

    grid_graph = GridGraph(resolution=1, minima=[-0.5, -0.5], extrema=[2.5, 2.5])
    grid_graph.create_edges()

    crime = Crime(0, 1, 'Car', 'nuit', 6, 2012)
    for _ in range(5):
        grid_graph.add_crime_occurrence(crime)

    crime = Crime(0, 2, 'Car', 'nuit', 6, 2009)
    for _ in range(10):
        grid_graph.add_crime_occurrence(crime)

    print(grid_graph.dict_representation()['nodes'])
    int_id = grid_graph.get_coordinates_grid_node_map()
    crime_node = grid_graph.find_closest_node(0, 2)
    for key, value in int_id.items():
        if value == crime_node.id:
            node_int = key

    p1 = grid_graph.filter(node_int, 3, 6)
    print(p1)