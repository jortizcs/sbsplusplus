import bind
import search
import EMD
import pandas as pd
import numpy as np
import os

f_range = 2

# days of data to process:
num_days = 1

# time bins: 6 hours
bins = 6

# number of time bins:
n = num_days * 24 / bins

if __name__ == '__main__':
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice/'
    path_list = os.listdir(path)
    path_list.sort()

    d = len(path_list)
    for i in range(d):
        path_list[i] = path + path_list[i]
    count = 0

    for j in range(1, n + 1):
        cMatrix = []
        for filename1 in path_list:
            print count
            count = count +1
            for filename2 in path_list:
                # IMFs1 = bind.EMD().emd(bind.dataProcessing_byday(filename1, num_days))
                # IMFs2 = bind.EMD().emd(bind.dataProcessing_byday(filename2, num_days))
                IMFs1 = EMD.emd(bind.dataProcessing_byday(filename1, num_days))
                IMFs2 = EMD.emd(bind.dataProcessing_byday(filename2, num_days))
                cMatrix.append(bind.getcMatrix(bind.getCluster(IMFs1), bind.getCluster(IMFs2), f_range, j, n))
        C = np.array(cMatrix).reshape((d, d))
        df = pd.DataFrame(C)
        file_name = 'C_Rice_range' + str(num_days)+'_day_range' + str(f_range) + '_timebin' + str(j-1) + '.csv'
        df.to_csv('/Users/wuxiaodong/Desktop/'+file_name)
