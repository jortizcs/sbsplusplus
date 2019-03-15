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


def cooler_open_window_model(temperature_model):
    t_model = temperature_model
    c_model = []
    for i in range(1, len(t_model)):
        c_model.append(3)
    c_model.append(c_model[len(c_model)-1])
    return np.array(c_model)

def heater_open_window_model(temperature_model):
    t_model = temperature_model
    c_model = []
    for i in range(1, len(t_model)):
        c_model.append(1)
    c_model.append(c_model[len(c_model)-1])
    return np.array(c_model)

def cooler_compete_model(temperature_model):
    t_model = temperature_model
    c_model = []
    for i in range(0, len(t_model)/20):
        for j in range(1, 11):
            c_model.append(3)
        for k in range(1, 11):
            c_model.append(1)
    for h in range(0, len(t_model)%20):
        c_model.append(3)
    return c_model


def heater_compete_model(temperature_model):
    t_model = temperature_model
    h_model = []
    for i in range(0, len(t_model)/20):
        for j in range(1, 11):
            h_model.append(1)
        for k in range(1,11):
            h_model.append(3)
    for h in range(0, len(t_model)%20):
        h_model.append(1)
    return h_model


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

    c_model = cooler_model(t_model[0:200])
    h_model = heater_model(t_model[0:200])
    open_window_cooler = cooler_open_window_model(t_model[200:400])
    open_window_heater = heater_open_window_model(t_model[200:400])

    compete_model = cooler_compete_model(t_model[400:])
    compete_model2 = heater_compete_model(t_model[400:])

    mix_model_cooler = np.append(c_model, open_window_cooler)
    mix_model_cooler = np.append(mix_model_cooler, compete_model)
    mix_model_heater = np.append(h_model, open_window_heater)
    mix_model_heater = np.append(mix_model_heater, compete_model2)
    plt.subplot(311)
    plt.plot(date, raw, label='data')
    plt.plot(date, t_model, label='model')
    plt.ylabel('temperature')
    plt.legend()

    plt.subplot(312)
    plt.plot(date, mix_model_cooler, label='cooler load')
    plt.ylabel('cooler load')

    plt.subplot(313)
    plt.plot(date, mix_model_heater, label='heater load')
    plt.ylabel('heater load')

    plt.gcf().autofmt_xdate()

    plt.show()




