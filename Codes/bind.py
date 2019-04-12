import numpy as np
#from PyEMD import EMD
import math
import EMD
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.stats as stats
import pandas as pd

from scipy.interpolate import interp1d
from scipy.signal import hilbert, chirp


def getFrequency(signal):
    fs = 0.0011
    analytic_signal = hilbert(signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) / (2.0 * np.pi) * fs)
    return instantaneous_frequency


def correlation(x, y):
    cor = stats.pearsonr(x, y)[0]  # get the cor of two signals
    if not math.isnan(cor):
        return cor
    else:
        return 0.0


def getCluster(IMFs):
    frequencies = []  # frequency of each IMFs
    for imf in IMFs:
        frequency = getFrequency(imf)
        frequency = filter(lambda x: x >= 0, frequency)
        frequencies.append(np.array(frequency).mean())
    matrix = np.transpose(np.array(IMFs))
    frequencies = np.array(frequencies)
    matrixF = np.vstack((frequencies, matrix))

    # 4 time scale ranges
    range1 = 0.00000193
    range2 = 0.0000463
    range3 = 0.00083
    Range = [0, 0, 0, 0]

    for i in range(len(matrixF[0])):
        f = matrixF[0, i]
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


def getCluster2(IMFs):
    frequencies = []  # frequency of each IMFs
    for imf in IMFs:
        frequency = getFrequency(imf)
        frequency = filter(lambda x: x >= 0, frequency)
        frequencies.append(np.array(frequency).mean())
    matrix = np.transpose(np.array(IMFs))
    frequencies = np.array(frequencies)
    matrixF = np.vstack((frequencies, matrix))

    # 4 time scale ranges
    range1 = 0.00000193
    range2 = 0.0000463
    range3 = 0.00083
    Range = [0, 0, 0, 0]

    cluster1 = np.zeros((1, len(matrix[:, 0])))
    cluster2 = np.zeros((1, len(matrix[:, 0])))
    cluster3 = np.zeros((1, len(matrix[:, 0])))
    cluster4 = np.zeros((1, len(matrix[:, 0])))
    for i in range(len(matrixF[0])):
        f = matrixF[0, i]
        new = matrix[:,i]
        if f < range1:
            Range[0] = Range[0] + 1
            cluster1 += new
        if range1 < f < range2:
            Range[1] = Range[1] + 1
            cluster2 += new
        if range2 < f < range3:
            Range[2] = Range[2] + 1
            cluster3 += new
        if f > range3:
            Range[3] = Range[3] + 1
            cluster4 += new
    cluster = np.vstack((cluster1, cluster2, cluster3, cluster4)).transpose()
    return cluster


def getReference(matrix1, matrix2, timeRange):
    # number of time bins: n
    n = 6 * 4
    l = len(matrix1[:, 0])/n
    ref = []
    for i in range(0, n/3):
        ref.append(correlation(matrix1[i*l:(i+1)*l, timeRange], matrix2[i*l:(i+1)*l, timeRange]))
    ref = np.array(ref)
    return np.median(ref)


def getcMatrix(matrix1, matrix2, timeRange, t, n):
    # number of time bins: n

    l = len(matrix1[:, 0])/n
    return correlation(matrix1[(t-1)*l: t*l, timeRange], matrix2[(t-1)*l:t*l, timeRange])


def dataProcessing_from_to(file_path, start, end):
    start = start - 1
    end = end - 1
    skip = start * 24 * 4
    row = (end - start) * 24 * 4
    raw_data = pd.read_csv(file_path, names=['date', 'value'], skiprows=skip, nrows=row)

    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    # plt.plot(raw_data['date'], raw_data['value'], label=fileName)
    # plt.legend()
    return np.array(raw_data['value'])


def dataProcessing_byday(file_path, day):
    row = day * 24 * 4
    raw_data = pd.read_csv(file_path, names=['date', 'value'], nrows=row)

    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    #plt.plot(raw_data['date'], raw_data['value'], label=fileName)
    #plt.legend()
    return np.array(raw_data['value'])


def dataProcessing(file_path):
    raw_data = pd.read_csv(file_path,names=['date', 'value'])

    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    #plt.plot(raw_data['date'], raw_data['value'], label=fileName)
    #plt.legend()
    return np.array(raw_data['value'])


def plot(filePath,tb, more_than_one):
    raw_data = pd.read_csv(filePath,
                           names=['date', 'value'])

    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    if more_than_one is False:
        plt.plot(raw_data['date'], raw_data['value'], label=fileName)
    n = 10
    l = len(raw_data)/n
    start = raw_data.iloc[l*tb, 0]
    end = raw_data.iloc[l*tb + l, 0]
    #print start, end
    plt.axvspan(start, end, facecolor='#c63535', alpha=0.5)
    plt.legend()
    plt.show()


def band_pass_filter(IMFs):
    sampling_rate = 0.001111
    b, a = signal.iirdesign([0.04, 0.75], [0.03, 0.8], 2, 40)
    return signal.lfilter(b, a, IMFs)


if __name__ == '__main__':
    IMF1s = EMD.emd(dataProcessing('2_Mag_HW_Return_Temp.csv'))
    IMF2s = EMD.emd(dataProcessing('2_Mag_CHW_Supply_Temp.csv'))
    xf = np.fft.fft(IMF1s)
    xf_abs = np.fft.fftshift(abs(xf))
    N = 671 * 7
    axis_xf = np.linspace(-N / 2, N / 2 - 1, num=N)

    plt.plot(axis_xf, xf_abs)
    plt.axis('tight')
    plt.show()

    out = band_pass_filter(IMF1s)

    xf = np.fft.fft(out)
    xf_abs = np.fft.fftshift(abs(xf))
    axis_xf = np.linspace(-N / 2, N / 2 - 1, num=N)

    plt.plot(axis_xf, xf_abs)
    plt.axis('tight')
    plt.show()