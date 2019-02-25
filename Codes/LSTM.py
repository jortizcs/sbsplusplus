import matplotlib.pyplot as plt
import numpy as np
import time
import csv
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from sklearn.metrics import r2_score


def get_data(path_to_dataset='/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice/1st Floor Avg Space Humidity.csv', sequence_length=20):
    max_values = 1343
    with open(path_to_dataset) as f:
        data = csv.reader(f)
        bike = []
        nb_of_values = 0
        for line in data:
            try:
                bike.append(float(line[1]))
                nb_of_values +=1
            except ValueError:
                pass
            if nb_of_values >= max_values:
                break

    result = []
    for index in range(len(bike) - sequence_length):
        result.append(bike[index: index + sequence_length])
    result = np.array(result)

    # normalize data
    result_mean = result.mean()
    result -= result_mean
    print("Shift : ", result_mean)
    print("Data : ", result.shape)

    row = int(round(0.9 * result.shape[0]))
    train = result[:row, :]
    np.random.shuffle(train)
    X_train = train[:, :-1]
    y_train = train[:, -1]
    X_test = result[row:, :-1]
    y_test = result[row:, -1]

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    return [X_train, y_train, X_test, y_test]


def build_model():
        model = Sequential()
        layers = [1, 50, 100, 1]

        model.add(LSTM(
            layers[1],
            input_shape=(None, 1),
            return_sequences=True))
        model.add(Dropout(0.2))

        model.add(LSTM(
            layers[2],
            return_sequences=False))
        model.add(Dropout(0.2))

        model.add(Dense(
            layers[3]))
        model.add(Activation("linear"))

        start = time.time()
        model.compile(loss="mse", optimizer="rmsprop")
        print("Compilation Time : ", time.time() - start)
        return model


def run_network(model=None, data=None):
    epochs = 100  # R^2 is around 0.49

    if data is None:
        print('Loading data... ')
        X_train, y_train, X_test, y_test = get_data()
    else:
        X_train, y_train, X_test, y_test = data

    print('\nData Loaded. Compiling...\n')

    if model is None:
        model = build_model()

    try:
        model.fit(
            X_train, y_train,
            batch_size=512, nb_epoch=epochs, validation_split=0.05)
        predicted = model.predict(X_test)
        predicted = np.reshape(predicted, (predicted.size,))
    except KeyboardInterrupt:
        return model, y_test, 0

    try:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(y_test)
        plt.plot(predicted, label='prediction')
        plt.legend()
        plt.show()
    except Exception as e:
        print(str(e))
    print('R-Squared: %f' % (r2_score(y_test, predicted)))
    return model, y_test, predicted


if __name__ == '__main__':
    run_network()

