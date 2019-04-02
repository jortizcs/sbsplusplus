import numpy as np
import sys
sys.path.append('../')
import anomalies_through_time as att
import os


def ground_truth_check(sensor, thresholds):
    tp = 0
    fn = 0
    f = open('/Users/wuxiaodong/Dropbox/adaptive-anomalies/without_dup/bv/range1/spike/ground_truth.txt')
    bug_locations = f.readlines()[sensor+1].split("   ")[1][1:-2].split(' ')
    bug_list = []
    for item in bug_locations:
        bug_list.append(int(item)/24)

    noise_result = att.anomalies_with_noise(sensor, thresholds)

    for bug in bug_list:
        if noise_result[bug] is True:
            tp += 1
        else:
            fn += 1
    true_positive_rate = (tp+0.0)/(tp+fn)
    return true_positive_rate


if __name__ == '__main__':
    ground_truth_check(0, [1, 1, 1])
