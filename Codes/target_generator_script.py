import bind
import search
import EMD
import pandas as pd
import numpy as np
import os


def target_generator_from_to(start, end):
    path = '/home/ec2-user/sbs/Rice/'
    path_list = os.listdir(path)
    path_list.sort()

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
        for filename1 in path_list:
            for filename2 in path_list:
                IMFs1 = EMD.emd(bind.dataProcessing_from_to(filename1, start, end))
                IMFs2 = EMD.emd(bind.dataProcessing_from_to(filename2, start, end))
                cluster1 = bind.getCluster(IMFs1)
                cluster2 = bind.getCluster(IMFs2)

                cMatrix.append(bind.getcMatrix(bind.getCluster(IMFs1), bind.getCluster(IMFs2), f_range, j, n))
        C = np.array(cMatrix).reshape((d, d))
        df = pd.DataFrame(C)
        file_name = 'C_Rice_day'+str(day_count)+'_range' + str(f_range) + '_timebin' + str((j - 1) % 4) + '.csv'
        df.to_csv('/home/ec2-user/sbs/output/' + file_name)
        day_count = day_count + j / 4


if __name__ == '__main__':
    target_generator_from_to(2, 4)
