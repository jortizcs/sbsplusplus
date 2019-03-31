import pandas as pd
import numpy as np
import bind
import matplotlib.pyplot as plt
import search
import anomaly_count
from datetime import datetime
import transforms
import os

path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice/'


def plot_graph(sensor_name):
    file_path = path + sensor_name
    raw_data = pd.read_csv(file_path,
                           names=['date', 'value'])
    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    plt.plot(raw_data['date'], raw_data['value'], label=sensor_name)


def plot_pair_graphs(path1, path2):
    plt.subplot(211)
    plot_graph(path1)
    plt.subplot(212)
    plot_graph(path2)
    plt.show()


def plot_pair_graphs_with_shade(path1, path2, day, timebin):
    plt.subplot(211)
    plot_with_shade(path1, day, timebin)
    plt.subplot(212)
    plot_with_shade(path2, day, timebin)
    plt.gcf().autofmt_xdate()


def plot_pair_by_id(sensor1_id, sensor2_id):
    path_list = os.listdir(path)
    path_list.sort()
    plot_pair_graphs(path_list[sensor1_id], path_list[sensor2_id])


def plot_with_shade(sensor_name, day, timebin):
    file_path = path + sensor_name
    raw_data = pd.read_csv(file_path,
                           names=['date', 'value'])
    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    plt.plot(raw_data['date'], raw_data['value'], label=sensor_name)

    num_tb = 28
    l = len(raw_data) / num_tb
    tb = 4 * (day-1) + timebin
    start = raw_data.iloc[l * tb, 0]
    end = raw_data.iloc[l * tb + l, 0]
    # print start, end
    plt.axvspan(start, end, facecolor='#c63535', alpha=0.5)

    plt.legend()


def plot_with_shades(sensor_name, tb_list):
    file_path = path + sensor_name
    raw_data = pd.read_csv(file_path,
                           names=['date', 'value'])
    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    plt.plot(raw_data['date'], raw_data['value'], label=sensor_name)

    num_tb = 28
    l = len(raw_data) / num_tb
    for tb in tb_list:
        start = raw_data.iloc[l * tb, 0]
        end = raw_data.iloc[l * tb + l, 0]
        # print start, end
        plt.axvspan(start, end, facecolor='#c63535', alpha=0.5)
        plt.legend()


def plot_transformed_with_shades(sensor_name, tb_list):
    file_path = path + sensor_name
    raw_data = pd.read_csv(file_path,
                           names=['date', 'value'])
    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])

    raw_data['value'] = transforms.flip(raw_data['value'])
    plt.plot(raw_data['date'], raw_data['value'], label=sensor_name + '+flip')

    num_tb = 28
    l = len(raw_data) / num_tb
    for tb in tb_list:
        start = raw_data.iloc[l * tb, 0]
        end = raw_data.iloc[l * tb + l, 0]
        # print start, end
        plt.axvspan(start, end, facecolor='#c63535', alpha=0.5)
        plt.legend()


if __name__ == '__main__':
    sensor = '1st Floor Avg Space Humidity.csv'
    plot_graph(sensor)
    plt.show()
