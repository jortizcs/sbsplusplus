import pandas as pd
import numpy as np
import bind
import matplotlib.pyplot as plt
import search
import anomaly_count
from datetime import datetime
import transforms
import os


path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice/'


def plot_graph(sensor_name):
    file_path = path + sensor_name
    raw_data = pd.read_csv(file_path,
                           names=['date', 'value'])
    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    plt.plot(raw_data['date'], raw_data['value'], label=sensor_name)


def plot_pair_graphs(path1, path2):
    plt.subplot(211)
    plot_graph(path1)
    plt.subplot(212)
    plot_graph(path2)
    plt.show()


def plot_pair_graphs_with_shade(path1, path2, day, timebin):
    plt.subplot(211)
    plot_with_shade(path1, day, timebin)
    plt.subplot(212)
    plot_with_shade(path2, day, timebin)
    plt.gcf().autofmt_xdate()


def plot_pair_by_id(sensor1_id, sensor2_id):
    path_list = os.listdir(path)
    path_list.sort()
    plot_pair_graphs(path_list[sensor1_id], path_list[sensor2_id])


def plot_with_shade(sensor_name, day, timebin):
    file_path = path + sensor_name
    raw_data = pd.read_csv(file_path,
                           names=['date', 'value'])
    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    plt.plot(raw_data['date'], raw_data['value'], label=sensor_name)

    num_tb = 28
    l = len(raw_data) / num_tb
    tb = 4 * (day-1) + timebin
    start = raw_data.iloc[l * tb, 0]
    end = raw_data.iloc[l * tb + l, 0]
    # print start, end
    plt.axvspan(start, end, facecolor='#c63535', alpha=0.5)

    plt.legend()


def plot_with_shades(sensor_name, tb_list):
    file_path = path + sensor_name
    raw_data = pd.read_csv(file_path,
                           names=['date', 'value'])
    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    plt.plot(raw_data['date'], raw_data['value'], label=sensor_name)

    num_tb = 28
    l = len(raw_data) / num_tb
    for tb in tb_list:
        start = raw_data.iloc[l * tb, 0]
        end = raw_data.iloc[l * tb + l, 0]
        # print start, end
        plt.axvspan(start, end, facecolor='#c63535', alpha=0.5)
        plt.legend()


def plot_transformed_with_shades(sensor_name, tb_list):
    file_path = path + sensor_name
    raw_data = pd.read_csv(file_path,
                           names=['date', 'value'])
    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])

    raw_data['value'] = transforms.flip(raw_data['value'])
    plt.plot(raw_data['date'], raw_data['value'], label=sensor_name + '+flip')

    num_tb = 28
    l = len(raw_data) / num_tb
    for tb in tb_list:
        start = raw_data.iloc[l * tb, 0]
        end = raw_data.iloc[l * tb + l, 0]
        # print start, end
        plt.axvspan(start, end, facecolor='#c63535', alpha=0.5)
        plt.legend()


def manual_result(l1,l2,l3,l4):
    a = []
    b = []
    c = []
    for i in range(30):
        tp = l1[i]
        fn = l2[i]
        fp = l3[i]
        tn = l4[i]
        acc = (tp + tn) / 24.0
        recall = tp / (tp + fn + 0.0)
        if tp == 0:
            precision = 0
        else:
            precision = tp / (tp + fp + 0.0)
        a.append(acc)
        b.append(recall)
        c.append(precision)
    return a,b,c


def PR_curve(tau_list):
    import manul_performance as mp
    recall_list = []
    precision_list = []
    sensor = np.arange(30)
    ground_truth_matrix = mp.ground_truth_interface(sensor)
    for tau in tau_list:
        threshold = [tau, 1.4826]
        result = mp.ground_truth_check_multi(sensor, threshold, ground_truth_matrix)
        recall = manual_result(result[0],result[1], result[2], result[3])[1]
        precision = manual_result(result[0],result[1], result[2], result[3])[2]
        recall_list.append(np.average(recall))
        precision_list.append(np.average(precision))
    print recall_list
    print precision_list
    plt.plot(precision_list, recall_list, '-o')
    plt.plot(0.23, 0.37, '-*', label='RL')
    plt.xlabel('precision')
    plt.ylabel('recall')
    plt.legend()
    plt.savefig("/home/ec2-user/graphs/PR_curve.png")


def DDPG_result(l1, l2, l3, l4):
    a = []
    b = []
    c = []
    for i in range(30):
        tp = l1[i]
        fn = l2[i]
        fp = l3[i]
        tn = l4[i]
        acc = (tp + tn)/24.0
        recall = tp/(tp+fn+0.0)
        if tp ==0:
            precision = 0
        else:
            precision = tp/(tp+fp+0.0)
        a.append(acc)
        b.append(recall)
        c.append(precision)

    hist, bin_edges = np.histogram(a)
    cdf = np.cumsum(hist)
    plt.plot(cdf)
    plt.show()

    name_list = ['accuracy', 'recall', 'precision']
    x = list(range(len(a)))
    total_width, n = 0.8, 3
    width = total_width / n

    plt.bar(x, a, width=width, label='accuracy', fc='y')

    for i in range(len(x)):
        x[i] = x[i] + width

    plt.bar(x, b, width=width, label='recall', fc='r')

    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, c, width=width, label='precision', fc='b')
    plt.legend()
    plt.xlabel("sensor ID")
    print np.average(a)
    print np.average(b)
    print np.average(c)
    #plt.savefig("/Users/wuxiaodong/Dropbox/adaptive-anomalies/graphs/DDPG_flip_30_sid.png", dpi=600)
    plt.show()

if __name__ == '__main__':

    PR_curve([0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5])


