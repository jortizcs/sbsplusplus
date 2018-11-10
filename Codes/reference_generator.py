import bind
import search
import EMD
import pandas as pd
import numpy as np
import os

f_range = 2
num_days = 1

if __name__ == '__main__':
    os.chdir('/Users/wuxiaodong/Desktop/18fall/SpecialProblem/metadata/rice_test/')
    file_chdir = os.getcwd()

    filecsv_list = []
    for root, dirs, files in os.walk(file_chdir):
        for file in files:
            if os.path.splitext(file)[1] == '.csv':
                filecsv_list.append(file)
    d = len(filecsv_list)
    R = []
    i = 0
    for filename1 in filecsv_list:
        for filename2 in filecsv_list:
            # IMFs1 = bind.EMD().emd(bind.dataProcessing_byday(filename1, num_days))
            # IMFs2 = bind.EMD().emd(bind.dataProcessing_byday(filename2, num_days))
            IMFs1 = EMD.emd(bind.dataProcessing_byday(filename1, num_days))
            IMFs2 = EMD.emd(bind.dataProcessing_byday(filename2, num_days))
            cluster1 = bind.getCluster(IMFs1)
            cluster2 = bind.getCluster(IMFs2)
            R.append(bind.getReference(cluster1, cluster2, f_range))
        print filename1
    R = np.array(R).reshape((d, d))
    df = pd.DataFrame(R)
    file_name = 'R_Rice_'+str(num_days)+'_day_range'+str(f_range)+'.csv'
    df.to_csv('/Users/wuxiaodong/Desktop/18fall/SpecialProblem/'+file_name)