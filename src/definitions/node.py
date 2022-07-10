from __future__ import annotations
from src.definitions.crime import Crime
import numpy as np
import pandas as pd
from uuid import uuid4
import copy as cp
from typing import List, Tuple, Set

Coordinates = Tuple[float, float]


class Point (object):
    def __init__(self, lat: float, lon: float, id: str = None, zone_id: str = None):
        self.id = str(uuid4()) if not id else id  # randomly generated string
        self.zone_id = None if not zone_id else zone_id
        self.lat = lat
        self.lon = lon

    def get_coordinates(self):
        """
        Obtain the coordinates of the Node to display it on the map
        """
        return self.lat, self.lon

    def distance(self, lat: float, lon: float) -> float:
        return np.sqrt((self.lat - lat)**2 + (self.lon - lon)**2)

    def distance_node(self, other: Node) -> float:
        return self.distance(other.lat, other.lon)

    def dict_representation(self):
        return {
            "id": self.id,
            "zone_id": self.zone_id,
            "lat": self.lat,
            "lon": self.lon
        }

    def __str__(self) -> str:
        return f"id: {self.id}, latitude: {self.lat}, longitude: {self.lon}"


class Node (Point):
    def __init__(self, lat: float, lon: float, id: str = None, zone_id : str = None, neighbours: List[str] = None):
        super(Node, self).__init__(lat, lon, id, zone_id)
        self._neighbours = set()
        if neighbours:
            self._neighbours = set(neighbours)

    def add_neighbour(self, neighbour_id: str):
        if self.id != neighbour_id:
            self._neighbours.add(neighbour_id)

    def get_neighbours(self) -> Set[str]:
        return cp.copy(self._neighbours)

    def dict_representation(self):
        return {
            **super(Node, self).dict_representation(),
            "neighbours": list(self._neighbours)
        }


class Zone (object):

    def __init__(self, lat: float, lon: float, x: int, y: int, id: str = None,
                 crimes=None, num_police_station=0, num_fire_station=0):
        self.id = str(uuid4()) if not id else id  # randomly generated string
        self.lat = lat
        self.lon = lon
        self.x = x
        self.y = y
        self.num_police_station = num_police_station
        self.num_fire_station = num_fire_station
        self.crimes = []
        self.crimes_df = None
        self.total_crimes = 0
        self.month_to_prob_crime = {}
        self.time_to_prob_crime = {}
        self._neighbours = set()
        if crimes is not None:
            self.crimes = crimes

    def init_crimes_df(self):
        self.crimes_df = pd.DataFrame(self.crimes, columns=['type_of_crime', 'time_of_day', 'month', 'year'])
        self.total_crimes = len(self.crimes_df)
        # fill in time of day
        for i in ['jour', 'soir', 'nuit']:
            self.time_to_prob_crime[i] = len(self.crimes_df[self.crimes_df['time_of_day'] == i]) / self.total_crimes if self.total_crimes else 0
        for i in range(1, 13):
            self.month_to_prob_crime[i] = len(self.crimes_df[self.crimes_df['month'] == i]) / self.total_crimes if self.total_crimes else 0

    def get_surrounding_zone(self, resolution: float) -> List[Coordinates]:
        step = resolution / 2
        return [(self.lat - step, self.lon + step),
                (self.lat + step, self.lon + step),
                (self.lat + step, self.lon - step),
                (self.lat - step, self.lon - step)]

    def in_surrounding_zone(self, resolution: float, lat: float, lon: float):
        step = resolution / 2
        return (lat >= self.lat - step and lat <= self.lat + step and
                lon >= self.lon - step and lon <= self.lon + step)

    def add_crime_occurrence(self, crime: Crime):
        self.crimes.append(crime.simplified_representation())

    def filter(self, time_of_day, month):
        if self.crimes_df is None:
            self.init_crimes_df()
        #  part_df = self.crimes_df[(self.crimes_df['time_of_day'] == time_of_day) & (self.crimes_df['month'] == month)]
        try:
            prob_crime = self.time_to_prob_crime[time_of_day] * self.month_to_prob_crime[month]
        except KeyError as e:
            print('####', time_of_day, self.time_to_prob_crime, month, self.month_to_prob_crime)
            raise e
        return prob_crime

    def add_police_station(self):
        self.num_police_station += 1

    def add_fire_station(self):
        self.num_fire_station += 1

    def dict_representation(self):
        return {
            "zone_id": self.id,
            "lat": self.lat,
            "lon": self.lon,
            "x": self.x,
            "y": self.y,
            "num_police_station": self.num_police_station,
            "num_fire_station": self.num_fire_station,
            "crimes": self.crimes
        }


if __name__ == "__main__":
    a = Zone(-73.62677804694519, 45.567779812980355)
    b = Zone(-73.62677804694519, 45.56777981298)
    c = Zone(-73, 43)
    print(a.distance_node(b))
    a.add_neighbour(b.id)
    a.add_neighbour(c.id)
    crime = Crime(-73, 45, '3', 'day', 3, 2020)
    print(crime.dict_representation())
    a.add_crime_occurrence(crime)
    a.add_crime_occurrence(Crime(-73, 45, '2', 'night', 3, 2020))
    print(a.dict_representation())
