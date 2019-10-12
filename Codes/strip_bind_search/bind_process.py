import numpy as np
import pandas as pd
import math
import scipy.signal as signal
import scipy.stats as stats
from scipy.signal import hilbert, chirp


def correlation(x, y):
    cor = stats.pearsonr(x, y)[0]  # get the cor of two signals
    if not math.isnan(cor):
        return cor
    else:
        return 0.0


def get_frequency(raw, fs):
    #fs = 0.0011
    analytic_signal = hilbert(raw)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) / (2.0 * np.pi) * fs)
    return instantaneous_frequency


class bind(object):
    def __init__(self, input1, input2, fs, frequency_range, timebins_per_day, total_day):
        self.input1 = input1
        self.input2 = input2
        self.fs = fs
        self.frequency_range = frequency_range
        self.timebins_per_day = timebins_per_day
        self.total_day = total_day
        self.n = self.total_day * self.timebins_per_day

    def get_cluster(self, imfs):
        frequencies = []  # frequency of each IMFs
        for imf in imfs:
            frequency = get_frequency(imf, self.fs)
            frequency = filter(lambda x: x >= 0, frequency)
            frequencies.append(np.array(frequency).mean())
        matrix = np.transpose(np.array(imfs))
        frequencies = np.array(frequencies)
        matrixF = np.vstack((frequencies, matrix))

        # 4 time scale ranges
        range1 = 0.00000193 # 6 days
        range2 = 0.0000463  # 6 hours
        range3 = 0.00083    # 20 mins
        Range = [0, 0, 0, 0]

        cluster1 = np.zeros((1, len(matrix[:, 0])))
        cluster2 = np.zeros((1, len(matrix[:, 0])))
        cluster3 = np.zeros((1, len(matrix[:, 0])))
        cluster4 = np.zeros((1, len(matrix[:, 0])))
        for i in range(len(matrixF[0])):
            f = matrixF[0, i]
            new = matrix[:, i]
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

    def getReference(self):
        matrix1 = self.get_cluster(self.input1)
        matrix2 = self.get_cluster(self.input2)
        # total time bins:
        l = len(matrix1[:, 0]) / self.n
        ref = []
        for i in range(0, self.n):
            ref.append(correlation(matrix1[i * l:(i + 1) * l, self.frequency_range],
                                   matrix2[i * l:(i + 1) * l, self.frequency_range]))
        ref = np.array(ref)
        return np.median(ref)

    def getCmatrix(self, t):
        matrix1 = self.get_cluster(self.input1)
        matrix2 = self.get_cluster(self.input2)
        l = len(matrix1[:, 0]) / self.n
        return correlation(matrix1[(t - 1) * l: t * l, self.frequency_range], matrix2[(t - 1) * l:t * l, self.frequency_range])


