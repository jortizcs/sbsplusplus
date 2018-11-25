import pandas as pd
import numpy as np
import bind
import search
import os

path = '/Users/wuxiaodong/Desktop/test/'

# frequency range:
f_range = 2

# number of time bins:
n = 4

# constant b of MAD:
b = 1.4826


def read_Rmatrix():
    r_path = path + 'Rice/R/3day/R_Rice_3_day_range2.csv'
    df = pd.read_csv(r_path)
    R = df.values
    R = R[:, 1:]
    return R


def read_Cmatrix(set, timebin):
    if timebin > n-1:
        return 'error: timebin is out of range'
    c_path = path+'Rice/C/'
    path_list = os.listdir(c_path)
    path_list.sort()
    d = len(path_list)
    for i in range(d):
        path_list[i] = c_path + path_list[i]
    df = pd.read_csv(path_list[timebin])
    C = df.values
    C = C[:, 1:]
    return C


def get_Cmatrix_list(set):
    list = []
    for i in range(n):
        list.append(read_Cmatrix(set, i))
    return list


def count(R, C_list, timebin, threshold):
    R = np.array(R)
    if len(C_list) != n:
        return 'Error: C matrices are not enough.'
    sum = 0
    for i in range(len(R)):
        for j in range(len(R)):
            l = []
            for t in range(n):
                l.append(search.behaviorChange(R, C_list[t], i, j))
            MAD = search.MAD(l, b)
            if search.anomaly(l, MAD, threshold, timebin) is True:
                sum = sum + 1
                print 'anomaly is in: (' + str(i) + ', ' + str(j)+')'
    print 'anomalies: ', sum
    return sum


if __name__ == '__main__':
    R = read_Rmatrix()
    C_list = get_Cmatrix_list('Rice')
    count(R, C_list, 3, 3)
