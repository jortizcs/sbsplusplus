import pandas as pd
import numpy as np
import bind
import matplotlib.pyplot as plt
import search
import os
import plot_graphs

path = '/Users/wuxiaodong/Dropbox/adaptive-anomalies/'

# frequency range:
f_range = 2

# constant b of MAD:
b = 1.4826


def count_interface(R, C_list, day, timebin, threshold, option):
    if option == 1:
        return count_sp_day(R, C_list, day, timebin, threshold)
    else:
        return count_abn_sensor(R, C_list, day, timebin, threshold)


def read_Rmatrix(num_days):
    r_path = path + '/R/'+str(num_days)+'day/R_Rice_'+str(num_days)+'_day_range'+str(f_range) + '.csv'
    df = pd.read_csv(r_path)
    R = df.values
    R = R[:, 1:]
    return R


def read_Cmatrix(set, day, timebin):
    c_path = path+'C/'
    path_list = os.listdir(c_path)
    path_list.sort()
    d = len(path_list)
    for i in range(d):
        path_list[i] = c_path + path_list[i]
    order = (day-1) * 4 + timebin
    df = pd.read_csv(path_list[order])
    C = df.values
    C = C[:, 1:]
    return C


def get_Cmatrix_list(set):
    list = []
    for day in range(1, 7):
        for tb in range(0, 4):
            list.append(read_Cmatrix(set, day, tb))
    return list


def count_sp_day(R, C_list, day, timebin, threshold):
    R = np.array(R)
    sum = 0
    tb = (day-1) * 4 + timebin
    for i in range(0, len(R)):
        for j in range(i+1, len(R)):
            l = []
            for c_matrix in C_list:
                l.append(search.behaviorChange(R, c_matrix, i, j))
            MAD = search.MAD(l, b)
            if search.anomaly(l, MAD, threshold, tb) is True:
                sum = sum + 1
    return sum/2


def count(R, C_list, timebin, threshold):
    R = np.array(R)
    sum = 0
    for i in range(0, len(R)):
        for j in range(i+1, len(R)):
            l = []
            for c_matrix in C_list:
                l.append(search.behaviorChange(R, c_matrix, i, j))
            MAD = search.MAD(l, b)
            if search.anomaly(l, MAD, threshold, timebin) is True:
                sum = sum + 1
    return sum/2


def count_abn_sensor(R, C_list, day, timebin, threshold):
    R = np.array(R)
    abn_sensors = []
    tb = (day-1)*4 + timebin
    for i in range(0, len(R)):
        l_i = []
        for c_matrix in C_list:
            l_i.append(search.behaviorChange_old(R, c_matrix, i))
        MAD = search.MAD(l_i, b)

        if search.anomaly(l_i, MAD, threshold, timebin) is True:
            print 'Abnormal behavior in sensor: ' + str(i)
            abn_sensors.append(i)
    return abn_sensors


def anomaly_check(R, abn_sensors, day, timebin):
    control_sensors = []
    correct = 0
    false = 0
    for sensor in abn_sensors:
        R_array = np.array(R)
        sensor_array = R_array[:, sensor]
        control_sensor = find_second_largest_index(sensor_array, sensor)
        control_sensors.append(control_sensor)
    for i in range(len(abn_sensors)):
        plot_graphs.plot_pair_by_id(abn_sensors[i], control_sensors[i], day, timebin)
        plt.show()
        print 'Press 1 for correct, 2 for false'
        check = int(raw_input())
        if check == 1:
            correct +=1
        else:
            false +=1
    print 'The correct anomalies are in total: '
    print correct
    print 'The false anomalies are in total: '
    print false


def find_second_largest_index(array, sensor):
    second_largest = -1
    index = 0
    for i in range(len(array)):
        if i != sensor:
            if array[i] > second_largest:
                second_largest = array[i]
                index = i
    return index


def detail_cell(R, C_list, day, timebin, threshold):
    R = np.array(R)
    sum = 0
    tb = (day-1) * 4 + timebin
    for i in range(0, len(R)):
        for j in range(i+1, len(R)):
            l = []
            for c_matrix in C_list:
                l.append(search.behaviorChange(R, c_matrix, i, j))
            MAD = search.MAD(l, b)
            if search.anomaly(l, MAD, threshold, tb) is True:
                sum = sum + 1
                print 'anomaly is in: (' + str(i) + ', ' + str(j)+')'
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
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice/'
    path_list = os.listdir(path)
    path_list.sort()
    print path_list