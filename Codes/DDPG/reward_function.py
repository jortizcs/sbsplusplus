import numpy as np
import sys
sys.path.append('../')
import anomalies_through_time as att
import os
import pandas as pd


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
    noise_result = att.anomalies_with_noise(sensor, 'flip_6hours_3', thresholds)

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

