import bind
import search
import EMD
import pandas as pd
import numpy as np
import os
import transforms
import noise_injection


f_range = 1

# days of data to process:
num_days = 6

# time bins: 6 hours
bins = 6

# number of time bins:
n = num_days * 24 / bins


def bv_generator():
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice_without_dup/'
    path_list = os.listdir(path)
    path_list.sort()

    d = len(path_list)
    for i in range(d):
        path_list[i] = path + path_list[i]
    count = 0
    bv_list = []
    for sensor in range(0, 1):
        day_count = 1
        bug_data = noise_injection.noise_inject_warp(sensor, 1)
        print 'sensor' + str(sensor)
        for j in range(1, n + 1):
            bv = []
            for filename1 in path_list:
                IMFs1 = EMD.emd(bind.dataProcessing_byday(filename1, num_days))
                IMFs2 = EMD.emd(bug_data)
                #IMFs2 = EMD.emd(bind.dataProcessing_byday(path_list[1], num_days))
                bv.append(bind.getcMatrix(bind.getCluster(IMFs1), bind.getCluster(IMFs2), f_range, j, n))
            bv = np.array(bv).reshape((d, 1))
            bv_list.append(bv)
            count+=1
            #print count
            print day_count
            df = pd.DataFrame(bv)
            file_name = 'BV_Rice_sensor_'+str(sensor)+'_warp_shrink_day' + str(day_count) + '_range' + str(f_range) + '_timebin' + str((j - 1) % 4) + '.csv'
            df.to_csv('/Users/wuxiaodong/Dropbox/adaptive-anomalies/without_dup/bv/range1/warp_shrink_1/sensor0/' + file_name)
            day_count = 1 + j / 4


if __name__ == '__main__':
    bv_generator()
