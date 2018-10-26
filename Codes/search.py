import numpy as np
import pandas as pd

from scipy.spatial import distance


def behaviorChange(refMatrix, cMatrix, deviceId):
    d = len(refMatrix[0])  # number of sensors
    R = refMatrix[:, deviceId]  # reference vector for deviceId
    C = cMatrix[:, deviceId]    # current vector for deviceId
    weight = abs(R / np.sum(R))  # weight of minkowski
    l = distance.minkowski(C, R, 4, weight)
    return l


def MAD(list, b):
    list = np.array(list)
    median = np.median(list)
    return b * np.median(np.abs(list - median))


def anomaly(list, MAD, threshold, t):
    if list[t] > np.median(list) + threshold * MAD:
        return True
    else:
        return False

