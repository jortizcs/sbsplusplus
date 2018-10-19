import bind
import search
import pandas as pd
import numpy as np
import os

if __name__ == '__main__':
    os.chdir('/Users/wuxiaodong/Desktop/18fall/SpecialProblem/data')
    file_chdir = os.getcwd()

    filescv_list = []
    for root, dirs, files in os.walk(file_chdir):
        for file in files :
            if os.path.splitext(file)[1] == '.csv':
                filescv_list.append(file)
    d = len(filescv_list)
    for i in range(0,4):
        R = []
        for filename1 in filescv_list:
            for filename2 in filescv_list:
                values1 = bind.dataProcessing(filename1)
                values2 = bind.dataProcessing(filename2)
                IMFs1 = bind.EMD().emd(values1)
                IMFs2 = bind.EMD().emd(values2)
                R.append(bind.getReference(bind.getCluster(IMFs1),bind.getCluster(IMFs2), i))
        R = np.array(R).reshape((d, d))
        print 'range', i
        print R


