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
        a.append(acc)
        if tp == 0 and fn == 0:
            b.append(1.)    # recall =1
        elif tp == 0 and fp == 0:
            c.append(1.)    # precision = 1
        else:
            recall = tp / (tp + fn + 0.0)
            b.append(recall)
            precision = tp / (tp + fp + 0.0)
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
        TPs = np.sum(result[0])
        FNs = np.sum(result[1])
        FPs = np.sum(result[2])
        TNs = np.sum(result[3])
        recall = TPs/(FNs+TPs+0.0)
        precision = TPs/(FPs + TPs + 0.0)
        recall_list.append(recall)
        precision_list.append(precision)
    print recall_list
    print precision_list
    print tau_list
    plt.plot(recall_list, precision_list, '-o')
    plt.plot(0.56, 0.13, '*', label='RL')
    plt.plot([0,1],[0,1], '--')
    plt.ylabel('precision')
    plt.xlabel('recall')
    plt.xlim([0,1])
    plt.ylim([0,1])
    plt.legend()
    plt.savefig("/home/ec2-user/graphs/PR_curve_shrink.png", dpi=600)


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
    #plt.plot(cdf)
    #plt.show()

    name_list = ['accuracy', 'recall', 'precision']
    x = list(range(len(a)))
    total_width, n = 0.8, 3
    width = total_width / n
    plt.rcParams.update({'font.size': 14})
    plt.bar(x, a, width=width, label='accuracy', fc='y')
    for i in range(len(x)):
        x[i] = x[i] + width

    plt.bar(x, b, width=width, label='recall', fc='r')

    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, c, width=width, label='precision', fc='b')
    plt.legend(fontsize = 14)
    #plt.legend(bbox_to_anchor=(1, 1), loc='center left', fontsize = 10)
    plt.xlabel("sensor ID")
    plt.ylim([0,1.4])
    my_y_ticks = np.arange(0, 1.2, 0.2)
    plt.yticks(my_y_ticks)
    print np.average(a)
    print np.average(b)
    print np.average(c)
    plt.savefig("/Users/wuxiaodong/Dropbox/adaptive-anomalies/graphs/DDPG_shrink_30_sid_PR.png", dpi=600)
    #plt.savefig("/home/ec2-user/sbsplusplus/DDPG_shrink_30_sid_pr.png", dpi=600)
    #plt.show()

if __name__ == '__main__':
    # import manul_performance as mp
    #
    # sensor = np.arange(30)
    # threshold = [1.8, 1.4826]
    # ground_truth_matrix = mp.ground_truth_interface(sensor)
    # result = mp.ground_truth_check_multi(sensor, threshold, ground_truth_matrix)
    # print result
    #DDPG_result(result[0], result[1], result[2], result[3])
    #tau_list = (np.arange(0,10, 0.2))
    #PR_curve(tau_list)
    plt.rcParams.update({'font.size': 14})
    recall_list = [0.7333333333333333, 0.7222222222222222, 0.6222222222222222, 0.5666666666666667, 0.4888888888888889, 0.4777777777777778, 0.4222222222222222, 0.37777777777777777, 0.3, 0.2222222222222222, 0.17777777777777778, 0.15555555555555556, 0.15555555555555556, 0.13333333333333333, 0.1111111111111111, 0.08888888888888889, 0.08888888888888889, 0.08888888888888889, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.05555555555555555, 0.044444444444444446, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.011111111111111112, 0.011111111111111112, 0.011111111111111112, 0.011111111111111112, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    precision_list =[0.1896551724137931, 0.23049645390070922, 0.23931623931623933, 0.2512315270935961, 0.2802547770700637, 0.31386861313868614, 0.3333333333333333, 0.37777777777777777, 0.3698630136986301, 0.37735849056603776, 0.38095238095238093, 0.3783783783783784, 0.4, 0.3870967741935484, 0.37037037037037035, 0.34782608695652173, 0.34782608695652173, 0.36363636363636365, 0.3157894736842105, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.35294117647058826, 0.35294117647058826, 0.3333333333333333, 0.3333333333333333, 0.2727272727272727, 0.2727272727272727, 0.375, 0.375, 0.375, 0.375, 0.42857142857142855, 0.5, 0.5, 0.25, 0.25, 0.3333333333333333, 0.3333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    plt.plot(recall_list, precision_list, '-o')
    plt.scatter(0.46, 0.36, s=120, marker='*', label='RL', color='y')
    plt.plot([0, 1], [0, 1], '--')
    plt.ylabel('precision')
    plt.xlabel('recall')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.legend(fontsize=16)
    plt.savefig("/Users/wuxiaodong/Dropbox/adaptive-anomalies/graphs/PR_curve_expand.png", dpi=600)
    plt.show()



