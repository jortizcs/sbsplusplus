import os
import pandas as pd
import numpy as np
from scipy.spatial import distance





class search(object):
    def __init__(self, R, R_path, C_path,timebins_per_day, tao, p, b):
        self.R = R
        self.R_path = R_path
        self.C_path = C_path
        self.timebins_per_day = timebins_per_day
        self.R = self.read_Rmatrix()
        self.C = self.read_Cmatrix()
        self.tao = tao
        self.p = p
        self.b = b

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

    def get_Cmatrix_list(self, start_date, end_date):
        list = []
        for day in range(start_date, end_date):
            for tb in range(0, self.timebins_per_day):
                list.append(self.read_Cmatrix(day, tb))
        return list

    def behavior_change(self, C, sensor_id):
        d = len(self.R[0])  # number of sensors
        R = self.R[:, sensor_id]  # reference vector for deviceId
        C = C[:, sensor_id]  # current vector for deviceId
        weight = abs(R / np.sum(R))  # weight of minkowski
        df = pd.DataFrame(weight).fillna(1)
        weight_arr = df.values
        l = distance.minkowski(C, R, self.p, weight_arr)
        return l

    def anomaly(self, list, MAD, t):
        if list[t] > np.median(list) + self.tao * MAD:
            return True
        else:
            return False

    def MAD(self, list, b):
        list = np.array(list)
        median = np.median(list)
        return b * np.median(np.abs(list - median))
