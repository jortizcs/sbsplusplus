import numpy as np
import pandas as pd

from scipy.spatial import distance


def behaviorChange(refMatrix, cMatrix, deviceId):
    d = len(refMatrix[0])
    R = refMatrix[:, deviceId]
    C = cMatrix[:, deviceId]
    weight = R / np.sum(R)
    l = distance.minkowski(C, R, 4, weight)


def MAD(list, b):
    median = np.median(list)
    return b * np.median(np.abs(list - median))


def anomaly(list, MAD, threshold, t):
    if list[t] > np.median(list) + threshold * MAD:
        return True
    else:
        return False

