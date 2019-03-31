import numpy as np
import pandas as pd
import os

if __name__ == '__main__':
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice_without_dup/'
    path_list = os.listdir(path)
    path_list.sort()
    name_list = path_list
    d = len(path_list)

    for i in range(d):
        path_list[i] = path + path_list[i]
        print path_list[i]

    for filename in path_list:
        raw_data = pd.read_csv(filename)
        raw_data = raw_data[1:][1:]
        df = pd.DataFrame(raw_data)
        df.to_csv()
