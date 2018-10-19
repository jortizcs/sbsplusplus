import numpy as np
from PyEMD import EMD
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.stats as stats
import pandas as pd

from scipy.interpolate import interp1d
from scipy.signal import hilbert, chirp


def getFrequency(signal):
    fs = 400.0
    analytic_signal = hilbert(signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) / (2.0 * np.pi) * fs)
    return instantaneous_frequency


def correlation(x, y):
    return stats.pearsonr(x, y)[0]  # get the cor of two signals


def getCluster(IMFs):
    frequencies = []  # frequency of each IMFs
    for imf in IMFs:
        frequency = getFrequency(imf)
        if frequency.mean()<0:
            frequencies.append(0.0)
        else:
            frequencies.append(frequency.mean())

    matrix = np.transpose(np.array(IMFs))
    frequencies = np.array(frequencies)
    matrixF = np.vstack((frequencies, matrix))

    # 4 time scale ranges
    range1 = 3
    range2 = 20
    range3 = 80
    Range = [0, 0, 0, 0]
    for f in matrixF[0, :]:
        if f < range1:
            Range[0] = Range[0] + 1
        if range1 < f < range2:
            Range[1] = Range[1] + 1
        if range2 < f < range3:
            Range[2] = Range[2] + 1
        if f > range3:
            Range[3] = Range[3] + 1
    cluster1 = np.sum(matrix[:, 0:Range[0]], 1)
    cluster2 = np.sum(matrix[:, Range[0]:Range[0] + Range[1]], 1)
    cluster3 = np.sum(matrix[:, Range[0] + Range[1]:Range[0] + Range[1] + Range[2]], 1)
    cluster4 = np.sum(matrix[:, Range[0] + Range[1] + Range[2]:], 1)
    cluster = np.vstack((cluster1, cluster2, cluster3, cluster4)).transpose()
    return cluster


def getReference(matrix1, matrix2, timeRange):
    n = 10  # number of time bins
    l = len(matrix1[:, 0])/n
    ref = []
    for i in range(0, 10):
        ref.append(correlation(matrix1[i*l:(i+1)*l,timeRange],matrix2[i*l:(i+1)*l,timeRange]))
    ref = np.array(ref)
    return ref.mean()


def dataProcessing(fileName):

    raw_data = pd.read_csv('/Users/wuxiaodong/Desktop/18fall/SpecialProblem/'+fileName,
                           names=['date', 'value'])

    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    # plt.plot(raw_data['date'], raw_data['value'])
    # plt.show()
    return np.array(raw_data['value'])


if __name__ == '__main__':
    IMF1s = EMD().emd(dataProcessing('2_Mag_HW_Return_Temp.csv'))
    IMF2s = EMD().emd(dataProcessing('2_Mag_CHW_Supply_Temp.csv'))
    print getReference(getCluster(IMF1s), getCluster(IMF2s), 0)
