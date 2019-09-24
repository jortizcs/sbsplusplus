import numpy as np 
#import matplotlib.pyplot as plt
import scipy.signal as signal
import pandas as pd

from scipy.interpolate import interp1d
from scipy.signal import hilbert, chirp
from scipy import interpolate


def findpeaks(x):
    index = signal.argrelextrema(x,np.greater)[0]
    return index


def getspline(x):

    N = np.size(x)
    peaks = findpeaks(x)
    peaks = np.concatenate(([0], peaks))
    peaks = np.concatenate((peaks, [N - 1]))
    if len(peaks) <= 3:
        t = interpolate.splrep(peaks, y=x[peaks], w=None, xb=None, xe=None, k=len(peaks) - 1)
        return interpolate.splev(np.arange(N), t)
    t = interpolate.splrep(peaks, y=x[peaks])
    return interpolate.splev(np.arange(N), t)


def isMonotonic(x):
    maximas=findpeaks(x)
    minimas=findpeaks(-1*x)
    if (len(maximas) == 0)or(len(minimas) == 0):
        return True
    else:
        return False


def isImf(x):
    N = np.size(x)
    pass_zero = np.sum(x[0:N-2]*x[1:N-1]<0)
    peaks_num = np.size(findpeaks(x))+np.size(findpeaks(-x))
    if abs(pass_zero - peaks_num)>1:
        return False
    else:
        return True


def emd(x):
    imf = []
    while not isMonotonic(x):
        x1 = x
        while (not isImf(x1)):
            s1 = getspline(x1)          # upper envelope
            s2 = -getspline(-1*x1)      # lower envelope
            x2 = x1-(s1+s2)/2             # mean envelope
            x1 = x2
        imf.append(x1)
        x = x-x1
    imf.append(x)
    return imf
