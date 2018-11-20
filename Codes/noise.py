import numpy as np
import pandas as pd
import os
import bind




def gauss_noise(signal):
    noise = np.random.normal(0, 0.000001, len(signal))
    return noise+signal


if __name__ == '__main__':
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice/'
    path_list = os.listdir(path)
    path_list.sort()
    name_list = path_list
    d = len(path_list)

    for i in range(d):
        path_list[i] = path + path_list[i]
        print path_list[i]

    for filename in path_list:
        raw_data = pd.read_csv(filename, names=['date', 'value'])
        raw_value = raw_data['value']
        if raw_value[0] == raw_value[1]:
            new_value =gauss_noise(np.array(raw_value))
            raw_data['value'] = new_value
            del raw_data.index.name
            raw_data.to_csv(filename, header=None, index=None)