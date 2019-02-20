import bind
import search
import EMD
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import plot_graphs



f_range = 1

# days of data to process:
num_days = 6

# time bins: 6 hours
bins = 6

# number of time bins:
n = num_days * 24 / bins

sensor1 = 170
sensor2 = 16

if __name__ == '__main__':
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice/'
    path_list = os.listdir(path)
    path_list.sort()

    d = len(path_list)
    for i in range(d):
        path_list[i] = path + path_list[i]

    c_values = []
    r_values = []
    for j in range(1, 25):
        IMFs1 = EMD.emd(bind.dataProcessing_byday(path_list[sensor1], 6))
        IMFs2 = EMD.emd(bind.dataProcessing_byday(path_list[sensor2], 6))
        cluster1 = bind.getCluster(IMFs1)
        cluster2 = bind.getCluster(IMFs2)
        #r_values.append(bind.getReference(cluster1, cluster2, f_range, n))
        c_values.append(bind.getcMatrix(cluster1, cluster2, f_range, j, n))

    plt.subplot(221)
    plt.hist(c_values, [-1, -0.5, 0, 0.5, 1])

    # obtain histogram data
    plt.subplot(222)
    hist, bin_edges = np.histogram(c_values, [-1, -0.5, 0, 0.5, 1])
    plt.plot(hist)


    plt.show()

    print c_values
