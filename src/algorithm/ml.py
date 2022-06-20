import tensorflow as tf
from tensorflow import keras
assert tf.__version__ >= "0.20"
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
tf.random.set_seed(42)
np.random.seed(42)


X = pd.read_csv('../../data/node_data_test.csv', sep=',', encoding='latin-1')
y = pd.read_csv('../../data/target_test.csv', sep=',', encoding='latin-1')
X = X[['time_of_day', 'month_of_year', 'node_number']]
y = y[['target']]['target']


X_train, X_valid, X_test = X[:1200], X[1200:1600], X[1600:]
y_train, y_valid, y_test = y[:1200]*100, y[1200:1600]*100, y[1600:]*100  # change probability to be percentage
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_valid = scaler.transform(X_valid)
X_test = scaler.transform(X_test)

model = keras.models.Sequential([
    keras.layers.Dense(100, activation="sigmoid", kernel_initializer="he_normal", input_shape=X_train.shape[1:]),
    keras.layers.Dense(30, activation="sigmoid", kernel_initializer="he_normal"),
    keras.layers.Dense(1)
])

model.compile(loss="mean_squared_error", optimizer=keras.optimizers.SGD(learning_rate=1e-1), metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=100, validation_data=(X_valid, y_valid))
mse_test = model.evaluate(X_test, y_test)


if __name__ == '__main__':
    print(mse_test)
    # from sklearn.linear_model import LinearRegression
    #
    # regressor = LinearRegression()
    # regressor.fit(X_train, y_train)
    #
    # # predicting the test set result
    y_pred = model.predict(X_train)
    df = pd.DataFrame(list(zip(y_train, y_pred)), columns=['Actual', 'Predicted'])
    df1 = df.head(30)
    print(df1)
    # # evaluate the performance of the algorithm (MAE - MSE - RMSE)
    # from sklearn import metrics
    # print('MAE:', metrics.mean_absolute_error(y_test, y_pred))
    # print('MSE:', metrics.mean_squared_error(y_test, y_pred))
    # print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    # print('VarScore:', metrics.explained_variance_score(y_test, y_pred))

