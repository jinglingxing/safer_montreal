from crime import Crime
from node import Node, Zone, Coordinates, Point
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


class MapGraph(Graph):

    def __init__(self,
                 resolution: float = None,
                 crime_data: pd.DataFrame = None,
                 roads: List[Dict] = None,
                 police_station_json: List[Dict] = None,
                 fire_station_json: List[Dict] = None,
                 json: dict = None):
        super().__init__()
        self._zones: Dict[str, Zone] = dict()
        self._zone_coordinates_to_id: Dict[Tuple[int, int], str] = dict()
        self._police_stations: Dict[str, Point] = dict()
        self._fire_stations: Dict[str, Point] = dict()

        # if we preprocessed the graph and saved it in json form, read it.
        if json:
            self.resolution = json['resolution']
            print('### processing nodes')
            total_nodes = len(json['nodes'])
            for index, element in enumerate(json['nodes']):
                print('processing node number ', index, 'over ', total_nodes)
                self._nodes[element['id']] = Node(element['lat'], element['lon'],
                                                  element['id'], element['zone_id'], element['neighbours'])
            print('### processing zones')
            total_zones = len(json['zones'])
            for index, element in enumerate(json['zones']):
                print('processing zone number ', index, 'over ', total_zones)
                self._zones[element['zone_id']] = Zone(element['lat'], element['lon'],
                                                     element['x'], element['y'],
                                                     element['zone_id'], element['crimes'],
                                                     element['num_police_station'], element['num_fire_station'])
            self._zone_coordinates_to_id = {eval(k): v for k, v in json['zone_coordinates_to_id'].items()}

            print('### processing police stations')
            total_police_stations = len(json['police_stations'])
            for index, element in enumerate(json['police_stations']):
                print('processing police station', index, 'over', total_police_stations)
                self._police_stations[element['id']] = Point(element['lat'], element['lon'], element['id'],
                                                             element['zone_id'])

            print('### processing fire stations')
            total_police_stations = len(json['fire_stations'])
            for index, element in enumerate(json['fire_stations']):
                print('processing fire station', index, 'over', total_police_stations)
                self._fire_stations[element['id']] = Point(element['lat'], element['lon'], element['id'],
                                                           element['zone_id'])
            return

        # normal initialization, with all the preprocessing
        self.resolution = resolution

        # manage cross-roads and edges
        self.min_lat = self.min_lon = 10000
        self.max_lat = self.max_lon = -10000
        for element in roads:
            print('processing road ', element['properties']['NOM_VOIE'])
            coordinates = element['geometry']['coordinates']
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


        # add node in map graph
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
                zone = self.add_zone(lat, lon, counter_x, counter_y)
                self._zone_coordinates_to_id[(counter_x, counter_y)] = zone.id
                print('added zone node : ', zone.id)
                y_min += resolution
                counter_y += 1
            y_min = y_minimal
            counter_x += 1

        # ingestion of crimes into our Zone objects
        for i in range(len(crime_data)):
            crime = Crime(crime_data.iloc[i]['LATITUDE'], crime_data.iloc[i]['LONGITUDE'],
                          crime_data.iloc[i]['CATEGORIE'], crime_data.iloc[i]['QUART'],
                          crime_data.iloc[i]['CRIME_MONTH'], crime_data.iloc[i]['CRIME_YEAR'])
            self.add_crime_occurrence(crime)
            print('ingested crime ', i, 'over ', len(crime_data))

        # find a corresponding zone to all the nodes
        inside_montreal = set()
        for node in self._nodes.values():
            print('finding corresponding zone to node ', node.id)
            try:
                inside_montreal.add(self.link_point_to_zone(node))
            except KeyError:
                print('ERROR:', node.lat, node.lon)
                raise KeyError

        # clean zones outside montreal
        outside_montreal = self._zones.keys() - inside_montreal
        for _id in outside_montreal:
            print('removing node ', _id)
            if len(self._zones[_id].crimes):
                print(self._zones[_id].crimes)
                #raise ValueError
            zone = self._zones[_id]
            del self._zone_coordinates_to_id[(zone.x, zone.y)]
            del self._zones[_id]

        for element in police_station_json:
            lon, lat = element['geometry']['coordinates']
            ps = Point(lat, lon)
            try:
                zone_id = self.link_point_to_zone(ps)
                self._police_stations[ps.id] = ps
                self._zones[zone_id].add_police_station()
            except KeyError:
                continue

        for element in fire_station_json:
            lon, lat = element['geometry']['coordinates']
            fs = Point(lat, lon)
            try:
                zone_id = self.link_point_to_zone(fs)
                self._fire_stations[fs.id] = fs
                self._zones[zone_id].add_fire_station()
            except KeyError:
                continue

    def check_extremum(self, lat, lon):
        if lat <= self.min_lat:
            self.min_lat = lat
        if lon <= self.min_lon:
            self.min_lon = lon
        if lat >= self.max_lat:
            self.max_lat = lat
        if lon >= self.max_lon:
            self.max_lon = lon

    def link_point_to_zone(self, node: Point) -> str:
        for zone in self._zones.values():
            node_zone = zone.in_surrounding_zone(self.resolution, node.lat, node.lon)
            if node_zone:
                node.zone_id = zone.id
                return zone.id
        raise KeyError

    def add_zone(self, lat: float, lon: float, x: int, y: int) -> Zone:
        zone = Zone(lat, lon, x, y)
        self._zones[zone.id] = zone
        return zone

    def get_zone_coordinates_to_id(self):
        return cp.copy(self._zone_coordinates_to_id)

    def add_crime_occurrence(self, crime: Crime):
        for zone in self._zones.values():
            node_zone = zone.in_surrounding_zone(self.resolution, crime.lat, crime.lon)
            if node_zone:
                zone.add_crime_occurrence(crime)
                break  # A crime belongs to only one Zone

    @jit
    def filter(self, x, y, time_of_day, month):
        reverse_map = {1: 'jour', 2: 'soir', 3: 'nuit'}
        time_of_day = reverse_map[time_of_day]
        node_id = self._zone_coordinates_to_id[(x, y)]
        zone = self._zones[node_id]
        node_prob_crimes = zone.filter(time_of_day, month)
        total_crimes = zone.total_crimes

        if not node_prob_crimes:
            return 0
        max = 0
        for zone in self._zones.values():
            crimes = zone.total_crimes
            if crimes > max:
                max = crimes
        probability = node_prob_crimes * float(total_crimes)/max if max else 0
        return probability

    def get_partial_input(self, node: Node):
        zone = self._zones[node.zone_id]
        return zone.x, zone.y, None, None

    def dict_representation(self):
        return {
            "resolution": self.resolution,
            "zone_coordinates_to_id": {str(k): v for k, v in self.get_zone_coordinates_to_id().items()},
            "nodes": [node.dict_representation() for node in self._nodes.values()],
            "zones": [zone.dict_representation() for zone in self._zones.values()],
            "police_stations": [ps.dict_representation() for ps in self._police_stations.values()],
            "fire_stations": [ps.dict_representation() for ps in self._fire_stations.values()]
        }


if __name__ == '__main__':

    grid_graph = MapGraph(resolution=1, minima=[-0.5, -0.5], extrema=[2.5, 2.5])
    grid_graph.create_edges()

    crime = Crime(0, 1, 'Car', 'nuit', 6, 2012)
    for _ in range(5):
        grid_graph.add_crime_occurrence(crime)

    crime = Crime(0, 2, 'Car', 'nuit', 6, 2009)
    for _ in range(10):
        grid_graph.add_crime_occurrence(crime)

    print(grid_graph.dict_representation()['nodes'])
    int_id = grid_graph.get_coordinates_zone_map()
    crime_node = grid_graph.find_closest_node(0, 2)
    for key, value in int_id.items():
        if value == crime_node.id:
            node_int = key

    p1 = grid_graph.filter(node_int, 3, 6)
    print(p1)