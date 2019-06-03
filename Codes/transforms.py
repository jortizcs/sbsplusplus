import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import signal as scipy_signal


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
    warping_signal = scipy_signal.resample(signal, len(signal)*2)
    return np.array(warping_signal[0:len(warping_signal)/2])


def warp_expand(signal):
    warping_signal = scipy_signal.resample(signal, len(signal)/2)

    return np.append(warping_signal,warping_signal)


if __name__ == '__main__':
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice_without_dup/'
    path_list = os.listdir(path)
    path_list.sort()
    raw_data = pd.read_csv(path+path_list[0],
                           names=['date', 'value'])
    values = raw_data['value']

    warped = warp_shrink(values[1:20])
    plt.plot(warped)
    plt.plot(np.array(values[1:20]))
    plt.show()

