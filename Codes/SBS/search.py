import os
import pandas as pd
import numpy as np


def MAD(list, b):
    list = np.array(list)
    median = np.median(list)
    return b * np.median(np.abs(list - median))


class search(object):
    def __init__(self, R_path, C_path):
        self.R_path = R_path
        self.C_path = C_path
        self.R = self.read_Rmatrix()
        self.C = self.read_Cmatrix()

    def read_Rmatrix(self):
        df = pd.read_csv(self.R_path)
        R = df.values
        R = R[:, 1:]
        return R

    def read_Cmatrix(self, day, timebin):
        c_path = self.C_path
        path_list = os.listdir(c_path)
        path_list.sort()
        d = len(path_list)
        for i in range(d):
            path_list[i] = c_path + path_list[i]
        order = (day - 1) * 4 + timebin
        df = pd.read_csv(path_list[order])
        C = df.values
        C = C[:, 1:]
        return C

    def get_Cmatrix_list(self):
        list = []
        for day in range(1, 5):
            for tb in range(0, 4):
                list.append(self.read_Cmatrix(day, tb))
        return list

    def behavior_change(self, sensor_id):
        d = len(self.R[0])  # number of sensors
        R = self.R[:, sensor_id]  # reference vector for deviceId
        C = self.C[:, sensor_id]  # current vector for deviceId
        weight = abs(R / np.sum(R))  # weight of minkowski
        df = pd.DataFrame(weight).fillna(1)
        weight_arr = df.values
        l = distance.minkowski(C, R, p, weight_arr)
        return l
