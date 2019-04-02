import os
import numpy as np
import pandas as pd
import transforms
import matplotlib.pyplot as plt

input_path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice_without_dup/'

output_path = 'Users/wuxiaodong/Desktop/Rice+noise/'

freq = 120


def get_path_list():
    path_list = os.listdir(input_path)
    path_list.sort()

    d = len(path_list)
    for i in range(d):
        path_list[i] = input_path + path_list[i]
    return path_list


def data_processing(sensor):
    path_list = get_path_list()
    raw_data = pd.read_csv(path_list[sensor], names=['date', 'value'])

    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    return np.array(raw_data['value'])


# freq: number of interval minutes
def segmentation(freq):
    interval = freq / 15
    return interval


def anomaly_location(num):
    interval = segmentation(freq)
    num_intervals = 576/interval

    locations = np.random.randint(288/interval, num_intervals, num)
    return locations


def noise_inject(sensor, num_of_noise):
    raw_data = data_processing(sensor)
    interval = segmentation(freq)
    location = anomaly_location(num_of_noise)
    location.sort()
    print location

    # save locations of noise
    f = open('/Users/wuxiaodong/Dropbox/adaptive-anomalies/without_dup/bv/range1/spike/ground_truth.txt', 'a')
    f.write('\n' + str(sensor) + '   ' +str(location * interval))

    for l in location:
        start = interval * l
        end = interval * (l+1)
        raw_data[start: end] = transforms.add_spike_noise(raw_data[start: end], 3)
    return raw_data


if __name__ == '__main__':
    data = noise_inject(162, 3)