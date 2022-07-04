import joblib
import keras
from typing import Tuple
from datetime import datetime
import pandas as pd


class Model(object):

    def __init__(self, decision_tree_path, neural_network_path, dt_scaler_path, nn_scaler_path, ohe_path):
        self.decision_tree = joblib.load(decision_tree_path)
        self.neural_network = keras.models.load_model(neural_network_path)
        self.dt_scaler = joblib.load(dt_scaler_path)
        self.nn_scaler = joblib.load(nn_scaler_path)
        self.ohe = joblib.load(ohe_path)

    @staticmethod
    def time_of_day(hour: int):
        if 6 <= hour <= 17:
            time = 1  # 'jour'
        elif 17 < hour <= 20:
            time = 2  # 'soir'
        else:
            time = 3  # 'nuit'
        return time

    def get_probability(self, partial_input: Tuple[int, int, int, int]):  # [ x, y, num_police_station, num_fire_station]
        now = datetime.now()
        month = now.month
        time_cat = self.time_of_day(now.hour)
        x, y, num_police_station, num_fire_station = partial_input

        one_hot_encoded_columns = pd.DataFrame([[time_cat, month]], columns=['time_of_day', 'month_of_year'])
        scaler_columns = pd.DataFrame([[x, y]], columns=['x', 'y'])

        l2 = self.dt_scaler.transform(scaler_columns)
        l1 = self.ohe.transform(one_hot_encoded_columns)

        input = l1+l2
        crime_or_not = self.decision_tree.predict([input])
        if not crime_or_not:
            return 0
        l3 = self.nn_scaler.transform(scaler_columns)
        input = l1+l3
        return self.neural_network.predict([input])




