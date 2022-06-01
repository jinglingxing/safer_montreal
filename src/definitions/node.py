from __future__ import annotations
from plotable import Plotable
from crime import Crime
import numpy as np
from uuid import uuid4
import copy as cp
from typing import List, Tuple
import matplotlib.pyplot as plt

Coordinates = Tuple[float, float]


class Node (Plotable):
    def __init__(self, lat: float, lon: float, id: str = None, crimes = None, neighbours: List[str] = None):
        self.id = str(uuid4()) if not id else id  # randomly generated string
        self.lat = lat
        self.lon = lon
        self.crimes = []
        self._neighbours = set()
        if crimes:
            self.crimes = crimes
        if neighbours:
            self._neighbours = neighbours

    def distance(self, lat: float, lon: float) -> float:
        return np.sqrt((self.lat - lat)**2 + (self.lon - lon)**2)

    def distance_node(self, other: Node) -> float:
        return self.distance(other.lat, other.lon)

    def add_neighbour(self, neighbour_id: str):
        if self.id != neighbour_id:
            self._neighbours.add(neighbour_id)

    def get_neighbours(self) -> List[Node]:
        return cp.copy(self._neighbours)

    def get_weight(self):
        # if not self._weight:
        #     for crime in self.crimes:
        #         self._weight += crime.get_weight()
        return len(self.crimes)

    def add_crime_occurrence(self, crime: Crime):
        self.crimes.append(crime.simplified_representation())

    def dict_representation(self):
        return {
            "id": self.id,
            "lat": self.lat,
            "lon": self.lon,
            "neighbours": list(self._neighbours),
            "crimes": self.crimes
        }

    def __str__(self) -> str:
        return f"id: {self.id}, latitude: {self.lat}, longitude: {self.lon}, weight: {self.get_weight()}"


class GridNode (Node):

    def get_surrounding_zone(self, resolution: float) -> List[Coordinates]:
        step = resolution / 2
        return [(self.lat - step, self.lon + step),
                (self.lat + step, self.lon + step),
                (self.lat + step, self.lon - step),
                (self.lat - step, self.lon - step)]

    def in_surrounding_zone(self, resolution: float, lat: float, lon: float):
        step = resolution / 2
        return (lat > self.lat - step and lat < self.lat + step and
                lon > self.lon - step and lon < self.lon + step)

    def node_plot(self, ax, color=None):
        if not color:
            color = 'b'
        ax.plot((self.lon), (self.lat), 'o', markersize=1, color=color)


if __name__ == "__main__":
    a = GridNode(-73.62677804694519, 45.567779812980355)
    b = GridNode(-73.62677804694519, 45.56777981298)
    c = GridNode(-73, 43)
    print(a.distance_node(b))
    a.add_neighbour(b.id)
    a.add_neighbour(c.id)
    crime = Crime(-73, 45, '3', 'day', 3, 2020)
    print(crime.dict_representation())
    a.add_crime_occurrence(crime)
    a.add_crime_occurrence(Crime(-73, 45, '2', 'night', 3, 2020))
    print(a.dict_representation())

    #print(a.get_neighbours())
    #print(a.in_surrounding_zone(0.02, -73.62677804694519, 45.56677981298))
    #fig = plt.figure()
    #ax = fig.add_subplot()
    #ax.autoscale(True)
    #a.node_plot(ax)
    #plt.show()
