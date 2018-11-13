import bind
import search
import EMD
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

if __name__ == '__main__':
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/data/'
    path_list = os.listdir(path)
    path_list.sort()
    name_list = path_list
    d = len(path_list)
    for i in range(d):
        path_list[i] = path + path_list[i]
        print path_list[i]

    # frequency range: i
    i = 2

    # num of days
    num_days = 0.25
    R = []
    cMatrix_list = []
    for r in range(0, 10):
        cMatrix_list.append([])
    for filename1 in path_list:
        for filename2 in path_list:
            #IMFs1 = bind.EMD().emd(bind.dataProcessing(filename1))
            #IMFs2 = bind.EMD().emd(bind.dataProcessing(filename2))
            IMFs1 = EMD.emd(bind.dataProcessing_byday(filename1, num_days))
            IMFs2 = EMD.emd(bind.dataProcessing_byday(filename2, num_days))
            cluster1 = bind.getCluster(IMFs1)
            cluster2 = bind.getCluster(IMFs2)
            R.append(bind.getReference(cluster1, cluster2, i))
            for j in range(1, 11):
                cMatrix_list[j - 1].append(bind.getcMatrix(bind.getCluster(IMFs1), bind.getCluster(IMFs2), i, j))
    R = np.array(R).reshape((d, d))
    cMatrix_list = np.array(cMatrix_list)

    print 'range', i
    print 'R: '
    print R
    print 'C: '
    for p in range(0, len(cMatrix_list)):
        print np.array(cMatrix_list[p]).reshape((d, d))
    plt.imshow(R, interpolation='nearest', cmap='bone')
    plt.colorbar()
    plt.xticks(())
    plt.yticks(())
    plt.show()

    # MAD:
    device = 0
    l_t = []
    for t in range(0, 10):
        l_t.append(search.behaviorChange(R, np.array(cMatrix_list[t]).reshape((d, d)), device))  # behavior changes for
        # device
    MAD = search.MAD(l_t, 1.4826)
    ano_list = []   # list to store the anomalies for each time bin
    threshold = 0.5
    for time in range(0, len(l_t)):
        an = search.anomaly(l_t, MAD, threshold, time)
        ano_list.append(an)
    print
    ano_list
    # plot the graph with anomalies for each pair of devices
    more_than_one = False   # in order to print the graph only once
    for item in range(0, len(ano_list)):
        if ano_list[item] is True:
            plt.subplot(211)
            bind.plot(name_list[device], item, more_than_one)
            plt.subplot(212)
            bind.plot(name_list[device+7], item, more_than_one)
            more_than_one = True
    plt.gcf().autofmt_xdate()
    plt.show()
