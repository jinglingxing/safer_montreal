

class Crime (object):

    def __init__(self, lon: float, lat: float, crime_type: str, time_of_day: str, month: int, year: int):
        self.lat = lat
        self.lon = lon
        self.type = crime_type
        self.time_of_day = time_of_day
        self.month = month
        self.year = year

    def get_weight(self):
        return self.type