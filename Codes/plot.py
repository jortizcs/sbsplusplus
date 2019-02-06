import pandas as pd
import numpy as np
import bind
import matplotlib.pyplot as plt
import search
import anomaly_count
from datetime import datetime
import os

path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice/'


def plot_graph(sensor_name):
    file_path = path + sensor_name
    raw_data = pd.read_csv(file_path,
                           names=['date', 'value'])

    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    plt.plot(raw_data['date'], raw_data['value'], label=sensor_name)
    plt.legend()


def plot_pair_graphs(path1,path2):
    plt.subplot(211)
    plot_graph(path1)
    plt.subplot(212)
    plot_graph(path2)
    plt.gcf().autofmt_xdate()


if __name__ == '__main__':
    path_list = os.listdir(path)
    path_list.sort()
    name_list = path_list
    d = len(path_list)
    plot_graph(name_list[0])
    #plot_pair_graphs(name_list[6], name_list[27])
    plt.show()

