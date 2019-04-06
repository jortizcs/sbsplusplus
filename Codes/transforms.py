import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


def add_gaussian_noise(signal, mu, sigma):
    noise = np.random.normal(mu, sigma, len(signal))
    return noise + signal


def add_spike_noise(signal, n):  # n: number of impulses
    signal = np.array(signal)
    impulse = np.random.randint(0, len(signal), n/2)
    for index in impulse:
        signal[index] += 0.6 * np.ptp(signal)
    impulse = np.random.randint(0, len(signal), n / 2)
    for index in impulse:
        signal[index] -= 0.6 * np.ptp(signal)
    return signal


def add_sap_noise(signal, m, n):  # m:number of white points; n: number of black points
    signal = np.array(signal)
    whites = np.random.randint(0, len(signal), m)
    blacks = np.random.randint(0, len(signal), n/2)
    blacks2 = np.random.randint(0, len(signal), n/2)

    for white in whites:
        signal[white] = np.mean(signal)
    for black in blacks:
        signal[black] += 0.6*np.ptp(signal)
        for black2 in blacks2:
            signal[black2] -= 0.6 * np.ptp(signal)
    return signal


def flip(signal):
    mean = np.mean(signal)
    for i in range(len(signal)):
        signal[i] = -(signal[i]-mean) + mean
    return signal


def warp_shrink(signal):
    signal = signal.set_index('date')
    warping_signal = signal.resample('30T').mean()
    return np.array(warping_signal['value'])


def warp_expand(signal):
    signal = signal.set_index('date')
    warping_signal = signal.resample('7.5T').pad()
    return np.array(warping_signal['value'])


if __name__ == '__main__':
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice_without_dup/'
    path_list = os.listdir(path)
    path_list.sort()
    raw_data = pd.read_csv(path+path_list[0],
                           names=['date', 'value'])
    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    raw_data = raw_data['value']
    warped = warp_expand(raw_data)
    warped2 = warp_shrink(raw_data)
    plt.plot(warped)
    plt.plot(np.array(raw_data['value']))
    plt.plot(warped2)
    plt.show()

