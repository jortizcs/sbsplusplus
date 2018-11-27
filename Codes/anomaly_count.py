import pandas as pd
import numpy as np
import bind
import matplotlib.pyplot as plt
import search
import os

path = '/Users/wuxiaodong/Dropbox/adaptive-anomalies/'

# frequency range:
f_range = 2

# number of time bins:
n = 4

# constant b of MAD:
b = 1.4826


def read_Rmatrix(num_days):
    r_path = path + '/R/'+str(num_days)+'day/R_Rice_'+str(num_days)+'_day_range'+str(f_range) + '.csv'
    df = pd.read_csv(r_path)
    R = df.values
    R = R[:, 1:]
    return R


def read_Cmatrix(set, timebin):
    if timebin > n-1:
        return 'error: timebin is out of range'
    c_path = path+'C/'
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
    for i in range(0, len(R)):
        for j in range(i+1, len(R)):
            l = []
            for t in range(n):
                l.append(search.behaviorChange(R, C_list[t], i, j))
            MAD = search.MAD(l, b)
            if search.anomaly(l, MAD, threshold, timebin) is True:
                sum = sum + 1
                print 'anomaly is in: (' + str(i) + ', ' + str(j)+')'
    print 'anomalies: ', sum
    return sum/2


def plot():
    threshold_list = range(1, 9, 1)
    for day in range(1, 4):
        R = read_Rmatrix(day)
        C_list = get_Cmatrix_list('Rice')
        anomalies = []
        for t in threshold_list:
            anomalies.append(count(R, C_list, 3, t))
        plt.plot(threshold_list, anomalies, label=str(day)+'day reference')
    plt.xlabel('threshold')
    plt.ylabel('anomalies')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    R = read_Rmatrix(3)
    C_list = get_Cmatrix_list('Rice')
    count(R, C_list, 3, 9)
