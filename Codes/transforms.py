import numpy as np


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
        signal[i] = -(signal[i]-mean) +mean
    return signal

