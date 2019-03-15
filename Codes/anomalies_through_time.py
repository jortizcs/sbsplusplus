import pandas as pd
import numpy as np
import bind
import matplotlib.pyplot as plt
import search
import anomaly_count
import behavior_vector_generator
from datetime import datetime
import os


def anomalies_throuth_time(sensor, threshold):
    b = 1.4826
    anomalies_list = []
    R = anomaly_count.read_Rmatrix(3)   # 3 days data as reference
    C_list = anomaly_count.get_Cmatrix_list('Rice')
    l_list = []
    for cmatrix in C_list:
        l_list.append(search.behaviorChange_old(R, cmatrix, sensor))
    MAD = search.MAD(l_list, b)
    for t in range(len(l_list)):
        anomalies_list.append(search.anomaly(l_list, MAD, threshold, t))
    print anomalies_list


def anomalies_with_transformed(sensor, threshold, noise):
    b = 1.4826
    anomalies_list = []
    R = anomaly_count.read_Rmatrix(3)  # 3 days data as reference
    bv_list = anomaly_count.read_bv_with_noise(sensor, noise)

    l_list = []
    for bv in bv_list:
        l_list.append(search.behavior_change_vector(R, bv, sensor))
    MAD = search.MAD(l_list, b)
    for t in range(len(l_list)):
        anomalies_list.append(search.anomaly(l_list, MAD, threshold, t))
    print anomalies_list


if __name__ == '__main__':
    anomalies_with_transformed(6, 1, "spike")
    anomalies_with_transformed(6, 1, "flip")
