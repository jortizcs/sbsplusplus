import pandas as pd
import numpy as np
import bind
import matplotlib.pyplot as plt
import search
import anomaly_count
from datetime import datetime
import os

if __name__ == '__main__':
    anomalies_list = []
    R = anomaly_count.read_Rmatrix(3)   # 3 days data as reference
    C_list = anomaly_count.get_Cmatrix_list('Rice')
    timebins = np.arange(0, len(C_list))
    for item in timebins:
        anomalies_list.append(anomaly_count.count(R, C_list, item, 9))
    #date_l = [datetime.strftime(x,'%Y-%m-%d') for x in list(pd.date_range(start='20160601', end='20160607'))]
    plt.plot(timebins, anomalies_list)
    plt.xlabel('time')
    plt.ylabel('anomalies')
    plt.legend()
    plt.show()