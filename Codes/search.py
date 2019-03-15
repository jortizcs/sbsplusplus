import numpy as np
import pandas as pd

from scipy.spatial import distance


def behaviorChange_old(refMatrix, cMatrix, deviceId):
    p = 4  # parameter for minkowski
    d = len(refMatrix[0])  # number of sensors
    R = refMatrix[:, deviceId]  # reference vector for deviceId
    C = cMatrix[:, deviceId]    # current vector for deviceId
    weight = abs(R / np.sum(R))  # weight of minkowski
    df = pd.DataFrame(weight).fillna(1)
    weight_arr = df.values
    l = distance.minkowski(C, R, p, weight_arr)
    return l


def behavior_change_vector(refMatrix, bvector, deviceId):
    p = 4  # parameter for minkowski
    d = len(refMatrix[0])  # number of sensors
    R = refMatrix[:, deviceId]  # reference vector for deviceId
    C = bvector  # current vector for deviceId
    weight = abs(R / np.sum(R))  # weight of minkowski
    df = pd.DataFrame(weight).fillna(1)
    weight_arr = df.values
    l = distance.minkowski(C, R, p, weight_arr)
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


def behaviorChange(refMatrix, cMatrix, device1, device2):
    return np.abs(refMatrix[device1, device2] - cMatrix[device1, device2])
