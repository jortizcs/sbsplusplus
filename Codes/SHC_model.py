from scipy import optimize
from scipy.optimize import leastsq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def raw_data():
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice/RMI503 Zone Temp 3.csv'
    raw_data = pd.read_csv(path,
                           names=['date', 'value'])
    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    data = np.array(raw_data['value'].values)
    return raw_data


def temperature_model(data):

    x = np.arange(0, len(data))
    A = 0.4
    w = 2*np.pi/100
    fi = 50
    B = 20.8
    model = A * np.sin(w*(x + fi))+B


    return model


def cooler_model(temperature_model):
    t_model = temperature_model
    c_model = []
    for i in range(1, len(t_model)):
        if t_model[i] > t_model[i-1]:
            c_model.append(3)
        else:
            c_model.append(1)
    c_model.append(c_model[len(c_model) - 1])
    return np.array(c_model)


def heater_model(temperature_model):
    t_model = temperature_model
    h_model = []
    for i in range(1, len(t_model)):
        if t_model[i] < t_model[i-1]:
            h_model.append(3)
        else:
            h_model.append(1)
    h_model.append(h_model[len(h_model)-1])
    return np.array(h_model)


if __name__ == '__main__':

    raw = np.array(raw_data()['value'].values)
    date = np.array(raw_data()['date'].values)
    t_model = temperature_model(raw)
    c_model = cooler_model(t_model)
    h_model = heater_model(t_model)
    plt.subplot(311)
    plt.plot(date, raw, label='data')
    plt.plot(date, t_model, label='model')
    plt.ylabel('temperature')
    plt.legend()

    plt.subplot(312)
    plt.plot(date, c_model, label='cooler load')
    plt.ylabel('cooler load')

    plt.subplot(313)
    plt.plot(date, h_model, label='heater load')
    plt.ylabel('heater load')
    plt.gcf().autofmt_xdate()

    plt.show()




