

class Crime (object):

    def __init__(self, lat: float, lon: float, crime_type: str, desc: str):
        self.lat = lat
        self.lon = lon
        self.type = crime_type
        self.desc = desc

    def get_weight(self):
        return self.type