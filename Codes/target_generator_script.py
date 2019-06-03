import bind
import search
import EMD
import pandas as pd
import numpy as np
import os


def target_generator_from_to(start, end):
    path = '/Users/wuxiaodong/Downloads/ydata-labeled-time-series-anomalies-v1_0/A1Benchmark/'
    path_list = os.listdir(path)
    path_list.sort(key=lambda x: int(x[5:-4]))
    print path_list

    f_range = 2

    # days of data to process:
    num_days = end - start

    # time bins: 6 hours
    bins = 6

    # number of time bins:
    n = num_days * 24 / bins

    d = len(path_list)
    for i in range(d):
        path_list[i] = path + path_list[i]
    count = 0
    day_count = start
    for j in range(1, n + 1):
        cMatrix = []
        print j
        for filename1 in path_list:
            for filename2 in path_list:
                #IMFs1 = EMD.emd(bind.dataProcessing_from_to(filename1, start, end))
                #IMFs2 = EMD.emd(bind.dataProcessing_from_to(filename2, start, end))
                #cluster1 = bind.getCluster(IMFs1)
                #cluster2 = bind.getCluster(IMFs2)

                arr1 = pd.read_csv(filename1, skiprows=288, nrows=24*4*num_days,names=['timepoint','value','gt'])['value'].values
                arr2 = pd.read_csv(filename2, skiprows=288, nrows=24*4*num_days,names=['timepoint','value','gt'])['value'].values
                IMFs1 = EMD.emd(arr1)
                IMFs2 = EMD.emd(arr2)

                cMatrix.append(bind.getcMatrix(bind.getCluster(IMFs1), bind.getCluster(IMFs2), f_range, j, n))
        C = np.array(cMatrix).reshape((d, d))
        df = pd.DataFrame(C)
        file_name = 'C_A1_day'+str(day_count)+'_range' + str(f_range) + '_timebin' + str((j - 1) % 4) + '.csv'
        df.to_csv('/Users/wuxiaodong/Dropbox/adaptive-anomalies/yahoo_dataset/C/' + file_name)
        day_count = day_count + j / 4


target_generator_from_to(4, 8)
