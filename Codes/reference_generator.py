import bind
import search
import EMD
import pandas as pd
import numpy as np
import os

f_range = 2
num_days = 3

if __name__ == '__main__':
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/data/'
    path_list = os.listdir(path)
    path_list.sort()

    d = len(path_list)
    for i in range(d):
        path_list[i] = path + path_list[i]
    count = 0
    R = []
    for filename1 in path_list:
        for filename2 in path_list:
            # IMFs1 = bind.EMD().emd(bind.dataProcessing_byday(filename1, num_days))
            # IMFs2 = bind.EMD().emd(bind.dataProcessing_byday(filename2, num_days))
            IMFs1 = EMD.emd(bind.dataProcessing_byday(filename1, num_days))
            IMFs2 = EMD.emd(bind.dataProcessing_byday(filename2, num_days))
            cluster1 = bind.getCluster(IMFs1)
            cluster2 = bind.getCluster(IMFs2)
            R.append(bind.getReference(cluster1, cluster2, f_range))
        count = count +1
        print count
    print len(R)
    R = np.array(R).reshape((d, d))
    print np.shape(R)
    df = pd.DataFrame(R)
    file_name = 'R_Rice_'+str(num_days)+'_day_range'+str(f_range)+'.csv'
    df.to_csv('/Users/wuxiaodong/Desktop/'+file_name)
