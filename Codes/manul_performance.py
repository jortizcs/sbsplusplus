import sys
sys.path.append('../')
import anomalies_through_time as att
import os
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import plot_graphs


def ground_truth_check_multi(sensors, thresholds, ground_truth):
    tp_total = []
    fn_total = []
    fp_total = []
    tn_total = []
    for sensor in sensors:
        i = 0
        (tp, fn, fp, tn) = ground_truth_check(sensor, thresholds[2*i:2*(i+1)], ground_truth[i])
        tp_total.append(tp)
        fn_total.append(fn)
        fp_total.append(fp)
        tn_total.append(tn)
        i += 1
    return tp_total, fn_total, fp_total, tn_total


def ground_truth_check(sensor, thresholds, ground_truth):
    tp = 0
    fn = 0
    fp = 0
    tn = 0

    bug_list = ground_truth
    noise_result = att.anomalies_with_noise(sensor, 'spike_6hours_3', thresholds)

    for a in range(len(noise_result)):
        if a in np.array(bug_list) and noise_result[a] is True:
            tp += 1
        elif a in np.array(bug_list) and noise_result[a] is False:
            fn += 1
        elif a not in np.array(bug_list) and noise_result[a] is True:
            fp += 1
        else:
            tn += 1

    return tp, fn, fp, tn


def ground_truth_check_yahoo(sensor, thresholds):
    tp = 0
    fn = 0
    fp = 0
    tn = 0
    path = '/Users/wuxiaodong/Dropbox/adaptive-anomalies/yahoo_dataset/A1Benchmark/'
    path_list = os.listdir(path)
    path_list.sort(key=lambda x: int(x[5:-4]))

    df = pd.read_csv(path +path_list[sensor])
    gt = df['is_anomaly'].values
    gt_list = []
    n = 3
    while n < len(gt)/24:
        for i in range(0, 24):
            if gt[24*n+i] == 1:
                gt_list.append(True)
                break
        gt_list.append(False)
        n += 1
    sbs_result = att.anomalies_through_time(sensor, thresholds)

    for a in range(len(sbs_result)):
        if gt_list[a] is True and sbs_result[a] is True:
            tp += 1
        elif gt_list[a] is True and sbs_result[a] is False:
            fn += 1
        elif gt_list[a] is False and sbs_result[a] is True:
            fp += 1
        else:
            tn += 1
    return tp, fn, fp, tn


def ground_truth_list(sensor):
    #f = open('/Users/wuxiaodong/Dropbox/adaptive-anomalies/noise_af_EMD/BV/spike_6hours_3/ground_truth.txt')
    f = open('/home/ec2-user/noise_af_EMD/BV/spike_6hours_3/ground_truth.txt')
    bug_locations = f.readlines()[sensor + 1].split("   ")[1][1:-2].split(' ')
    bug_list = []
    for item in bug_locations:
        bug_list.append(int(item) / 24)
    return bug_list


def ground_truth_interface(sensor):
    if len(sensor) == 1:
        return ground_truth_list(sensor)
    else:
        ground_truth_matrix = []
        for s in sensor:
            ground_truth_matrix.append(ground_truth_list(s))
        return ground_truth_matrix


sensor = np.arange(30)
threshold1 = [1, 1.4826]
threshold2 = [2, 1.4826]
threshold3 = [3, 1.4826]
threshold4 = [4, 1.4826]

ground_truth_matrix = ground_truth_interface(sensor)

result1 = ground_truth_check_multi(sensor, threshold1, ground_truth_matrix)
result2 = ground_truth_check_multi(sensor, threshold2, ground_truth_matrix)
result3 = ground_truth_check_multi(sensor, threshold3, ground_truth_matrix)
result4 = ground_truth_check_multi(sensor, threshold4, ground_truth_matrix)
result_rl = ([0, 2, 1, 0, 2, 1, 2, 0, 1, 2, 1, 1, 1, 1, 3, 1, 0, 3, 1, 0, 1, 0, 1, 2, 1, 1, 1, 1, 0, 3],

            [3, 1, 2, 3, 1, 2, 1, 3, 2, 1, 2, 2, 2, 2, 0, 2, 3, 0, 2, 3, 2, 3, 2, 1, 2, 2, 2, 2, 3, 0],

            [3, 6, 6, 3, 3, 2, 7, 3, 6, 4, 4, 2, 3, 2, 3, 2, 7, 4, 3, 0, 6, 4, 4, 1, 2, 3, 5, 7, 4, 3],

            [18, 15, 15, 18, 18, 19, 14, 18, 15, 17, 17, 19, 18, 19, 18, 19, 14, 17, 18, 21, 15, 17, 17, 20, 19, 18, 16, 14, 17, 18])

acc1 = plot_graphs.manual_result(result1[0],result1[1], result1[2], result1[3])[1]
acc2 = plot_graphs.manual_result(result2[0],result2[1], result2[2], result2[3])[1]
acc3 = plot_graphs.manual_result(result3[0],result3[1], result3[2], result3[3])[1]
acc4 = plot_graphs.manual_result(result4[0],result4[1], result4[2], result4[3])[1]
acc_rl = plot_graphs.manual_result(result_rl[0],result_rl[1], result_rl[2], result_rl[3])[1]

hist1, bin_edges1 = np.histogram(acc1)
cdf = np.cumsum(hist1.astype(float)/sum(hist1))
plt.plot(bin_edges1[1:], cdf, label=r'$\tau$ = '+str(threshold1[0]))

hist2, bin_edges2 = np.histogram(acc2)
cdf = np.cumsum(hist2.astype(float)/sum(hist1))
plt.plot(bin_edges2[1:], cdf, label=r'$\tau$ = '+str(threshold2[0]))

hist3, bin_edges3 = np.histogram(acc3)
cdf = np.cumsum(hist3.astype(float)/sum(hist3))
plt.plot(bin_edges3[1:], cdf, label=r'$\tau$ = '+str(threshold3[0]))

hist4, bin_edges4 = np.histogram(acc4)
cdf = np.cumsum(hist4.astype(float)/sum(hist4))
plt.plot(bin_edges4[1:], cdf, label=r'$\tau$ = '+str(threshold4[0]))

hist_rl, bin_edges_rl = np.histogram(acc_rl)
cdf = np.cumsum(hist_rl.astype(float)/sum(hist_rl))
#plt.plot(bin_edges_rl[1:], cdf, '-*', color='#ED7D31', label='RL')


plt.ylim([0, 1])
plt.legend()
plt.xlabel('recall')
plt.ylabel('cumulative dense probability')
plt.savefig('/home/ec2-user/cdf_1234_recall.png', dpi=600)
