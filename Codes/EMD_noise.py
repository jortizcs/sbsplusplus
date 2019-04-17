import bind
import search
import EMD
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import noise_injection
import anomalies_through_time

path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice_without_dup/'
path_list = os.listdir(path)
path_list.sort()
name_list = path_list
d = len(path_list)
for i in range(d):
    path_list[i] = path + path_list[i]



IMFs1 = EMD.emd(bind.dataProcessing_byday(path_list[0], 6))
bug_data = noise_injection.noise_inject(0, 3)
IMFs2 = EMD.emd(bug_data)
cluster1 = bind.getCluster2(IMFs2)

print anomalies_through_time.anomalies_without_noise(0, [1,1,1])
