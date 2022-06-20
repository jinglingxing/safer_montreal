import tensorflow as tf
from tensorflow import keras
assert tf.__version__ >= "0.20"
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


if __name__ == '__main__':
    tf.random.set_seed(42)
    np.random.seed(42)

    X = pd.read_csv('../../data/node_data.csv', sep=',', encoding='latin-1')
    y = pd.read_csv('../../data/target.csv', sep=',', encoding='latin-1')
    X = X[['time_of_day', 'month_of_year', 'node_number']]
    y = y[['target']]['target']

    sep1, sep2 = int(len(X)*0.7), int(len(X)*0.9)
    X_train, X_test, X_valid = X[:sep1], X[sep1:sep2], X[sep2:]
    y_train, y_test, y_valid = y[:sep1] * 10000, y[sep1:sep2]*10000, y[sep2:] * 10000  # change probability to be percentage
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_valid = scaler.transform(X_valid)
    X_test = scaler.transform(X_test)

    model = keras.models.Sequential([
        keras.layers.Dense(100, activation="sigmoid", kernel_initializer="he_normal", input_shape=X_train.shape[1:]),
        keras.layers.Dense(30, activation="sigmoid", kernel_initializer="he_normal"),
        keras.layers.Dense(1)
    ])

    model.compile(loss="mean_squared_logarithmic_error",
                  optimizer=keras.optimizers.SGD(learning_rate=1e-1),
                  metrics=['accuracy'])
    history = model.fit(X_train, y_train, epochs=100, validation_data=(X_valid, y_valid),
                        callbacks=[keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)])

    mse_test = model.evaluate(X_test, y_test)
    model.save("neural_network_full_datasets.h5")
    model = keras.models.load_model("neural_network_full_datasets.h5")
    # # predicting the test set result
    y_pred = model.predict(X_train)
    df = pd.DataFrame(list(zip(y_train, y_pred)), columns=['Actual', 'Predicted'])
    print(df.head(30))

