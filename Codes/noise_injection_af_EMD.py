import bind
import search
import EMD
import pandas as pd
import numpy as np
import noise_injection
import matplotlib.pyplot as plt
import os
import transforms


def noise_inject(signal, num_of_noises):
    freq = 360
    interval = freq / 15
    num_intervals = 576 / interval
    locations = np.random.randint(288 / interval, num_intervals, num_of_noises)
    locations.sort()

    # save locations of noise
    # f = open('/Users/wuxiaodong/Dropbox/adaptive-anomalies/noise_af_EMD/BV/spike_6hours_' + str(num_of_noises) +
    #          '/ground_truth.txt', 'a')

    f = open('/Users/wuxiaodong/Dropbox/adaptive-anomalies/noise_af_EMD/BV/flip_6hours_' + str(num_of_noises) +
              '/ground_truth.txt', 'a')
    f.write('\n' + str(sensor) + '   ' + str(locations * interval))

    for l in locations:
        start = interval * l
        end = interval * (l + 1)
        #signal[start: end] = transforms.add_spike_noise(signal[start: end], 10)
        signal[start: end] = transforms.flip(signal[start: end])
    return signal


def noise_inject_warp(signal, num_of_noise):
    freq = 360
    interval = freq / 15
    num_intervals = 576 / interval

    locations = np.random.randint(288 / interval, num_intervals, num_of_noise)
    locations.sort()

    f = open('/Users/wuxiaodong/Dropbox/adaptive-anomalies/noise_af_EMD/BV/warp_shrink_' + str(num_of_noise) +
             '/ground_truth.txt', 'a')
    f.write('\n' + str(sensor) + '   ' + str(locations * interval))

    for l in locations:
        start = interval * l
        end = interval * (l + 1)
        f1 = np.array(signal[:start])

        f2 = transforms.warp_shrink(signal[start: end])
        f3 = np.array(signal[end:])
        signal = np.concatenate((f1, f2, f3), axis=0)
    return signal


path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice_without_dup/'
path_list = os.listdir(path)
path_list.sort()

f_range = 2

# days of data to process:
num_days = 6

# time bins: 6 hours
bins = 6

# number of time bins:
n = num_days * 24 / bins


d = len(path_list)
for i in range(d):
    path_list[i] = path + path_list[i]
count = 0
bv_list = []

for sensor in range(0, 3):
    IMFs1 = EMD.emd(bind.dataProcessing_byday(path_list[sensor], num_days))
    cluster1 = bind.getCluster2(IMFs1)
    cluster1[:, 2] = noise_inject_warp(cluster1[:,2], 3)
    day_count = 1
    print 'sensor' + str(sensor)
    for j in range(1, n + 1):
        bv = []
        for filename1 in path_list:
            IMFs2 = EMD.emd(bind.dataProcessing_byday(filename1, num_days))
            cluster2 = bind.getCluster2(IMFs2)
            bv.append(bind.getcMatrix(cluster1, cluster2, 2, j, n))
        bv = np.array(bv).reshape((d, 1))
        bv_list.append(bv)
        count += 1
        print count
        print day_count
        df = pd.DataFrame(bv)
        file_name = 'BV_Rice_sensor_'+str(sensor)+'warp_shrink_3' + str(day_count) + '_range' + str(f_range) + '_timebin' + str((j - 1) % 4) + '.csv'
        df.to_csv('/Users/wuxiaodong/Dropbox/adaptive-anomalies/noise_af_EMD/BV/warp_shrink_3/sensor'+str(sensor)+'/' + file_name)
        day_count = 1 + j / 4


