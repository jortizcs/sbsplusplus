import pandas as pd
import os


if __name__ == '__main__':
    path = '/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice/'
    path_list = os.listdir(path)
    path_list.sort()
    name_list = path_list

    for file in path_list:
        raw_data = pd.read_csv(path+file, names=['date', 'value'])
        raw_data = raw_data.drop_duplicates('date')
        df = pd.DataFrame(raw_data)
        df.to_csv('/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Rice_without_dup/' + file, index=False, header=False)
