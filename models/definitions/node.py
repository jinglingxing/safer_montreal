from __future__ import annotations
from plotable import Plotable
from crime import Crime
import numpy as np
from uuid import uuid4
import copy as cp
from typing import List, Tuple

Coordinates = Tuple[float, float]


class Node (Plotable):
    def __init__(self, lat: float, lon: float):
        self.id = str(uuid4())
        self.lat = lat
        self.lon = lon
        self.crimes = []
        self._weight = 0
        self._neighbours = dict()

    def distance(self, other: Node) -> float:
        return np.sqrt((self.lat - other.lat)**2 + (self.lon - other.lon)**2)

    def add_neighbour(self, neighbour: Node):
        self._neighbours[neighbour.id] = neighbour

    def get_neighbours(self) -> List[Node]:
        return cp.copy(self._neighbours)

    def get_weight(self):
        if not self._weight:
            for crime in self.crimes:
                self._weight += crime.get_weight() 
            
        return self._weight

    def add_crime_occurrence(self, crime: Crime):
        self.crimes.append(crime)

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



if __name__ == "__main__":
    a = Node(-73.62677804694519, 45.567779812980355)
    b = Node(-73.62677804694519, 45.56777981298)
    print(a.distance(b))
    a.add_neighbour(b)
    l = a.get_neighbours()
    l[1] = 1
    print(a.get_neighbours())