import pandas as pd
import numpy as np
import bind
import search
import os

path = '/Users/wuxiaodong/Dropbox/adaptive-anomalies/csv/'

# number of time bins:
n = 4

def read_Rmatrix(set, num_days):
    path_list = os.listdir(path+str(set)+'/'+str(num_days)+'day/')
    path_list.sort()
    d = len(path_list)
    for i in range(d):
        path_list[i] = path + path_list[i]
    df = pd.read_csv(path)
    R = df.values
    return R


def read_Cmatrix(set, timebin):
    if timebin > n-1:
        return 'error: timebin is out of range'
    path_list = os.listdir(path+str(set)+'/'+str(timebin)+'timebin/')
    path_list.sort()
    d = len(path_list)
    for i in range(d):
        path_list[i] = path + path_list[i]
    df = pd.read_csv(path)
    C = df.values
    return C


def get_Cmatrix_list(set):
    list = []
    for i in range(n):
        list.append(read_Cmatrix(set, i))
    return list


def count(R, C_list, timebin, threshold):
    R = np.array(R)
    if len(C_list) != n:
        return 'Error: number of C matrices are not enough.'
    if R.shape != C_list[timebin].shape:
        return 'Error: R and C are not in the same dimension.'
    l = []
    for i in range(R.shape):
        for j in range(R.shape):
            for t in range(n):
                l.append(search.behaviorChange(R, C_list[timebin], i, j))


