import bind
import search
import EMD
import pandas as pd
import numpy as np
import os

f_range = 2

# number of time bins:
n = 4

if __name__ == '__main__':
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/data/'
    path_list = os.listdir(path)
    path_list.sort()

    d = len(path_list)
    for i in range(d):
        path_list[i] = path + path_list[i]
    count = 0

    for j in range(1, n + 1):
        cMatrix = []
        for filename1 in path_list:
            for filename2 in path_list:
                # IMFs1 = bind.EMD().emd(bind.dataProcessing_byday(filename1, num_days))
                # IMFs2 = bind.EMD().emd(bind.dataProcessing_byday(filename2, num_days))
                IMFs1 = EMD.emd(bind.dataProcessing(filename1))
                IMFs2 = EMD.emd(bind.dataProcessing(filename2))
                cluster1 = bind.getCluster(IMFs1)
                cluster2 = bind.getCluster(IMFs2)

                cMatrix.append(bind.getcMatrix(bind.getCluster(IMFs1), bind.getCluster(IMFs2), f_range, j))
        C = np.array(cMatrix).reshape((d, d))
        df = pd.DataFrame(C)
        file_name = 'C_Rice_range' + str(f_range) + '_timebin_' + str(j) + '.csv'
        df.to_csv('/Users/wuxiaodong/Desktop/'+file_name)
