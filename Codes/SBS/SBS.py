from EMD_process import emd
from bind_process import bind
from search import search
import os
import numpy as np
import pandas as pd


class SBS(object):
    def __init__(self, reference_path, test_path,  fs, frequency_range, timebins_per_day, total_day,
                 R_output_path, C_output_path):
        self.reference_path = reference_path
        self.test_path = test_path
        self.fs = fs
        self.frequency_range = frequency_range
        self.timebins_per_day = timebins_per_day
        self.total_day = total_day
        self.R = []
        self.C = []
        self.R_output_path = R_output_path
        self.C_output_path = C_output_path

        self.R_path_list = os.listdir(self.reference_path)
        self.R_path_list.sort()
        R_name_list = self.R_path_list
        self.d = len(self.R_path_list)
        for i in range(self.d):
            self.R_path_list[i] = self.reference_path + self.R_path_list[i]

        self.C_path_list = os.listdir(self.test_path)
        self.C_path_list.sort()
        C_name_list = self.C_path_list
        for i in range(self.d):
            self.C_path_list[i] = self.test_path + self.C_path_list[i]

    def R_generator(self):
        for filename1 in self.R_path_list:
            for filename2 in self.R_path_list:
                raw_data1 = pd.read_csv(filename1, names=['date', 'value'])
                raw_data2 = pd.read_csv(filename2, names=['date', 'value'])

                raw_data1['date'] = pd.to_datetime(raw_data1['date'], unit='s')
                raw_data2['date'] = pd.to_datetime(raw_data2['date'], unit='s')
                raw_data1 = raw_data1.sort_values(by=['date'])
                raw_data2 = raw_data2.sort_values(by=['date'])
                imfs1 = emd(np.array(raw_data1))
                imfs2 = emd(np.array(raw_data2))

                self.R.append(bind(imfs1, imfs2, self.fs, self.frequency_range, self.timebins_per_day, self.total_day)
                              .getReference())
        self.R = np.array(self.R).reshape((self.d, self.d))
        df = pd.DataFrame(self.R)
        file_name = 'Reference_Matrix_Range' + str(self.frequency_range) + '.csv'
        df.to_csv(self.R_output_path + file_name)

    def C_generator(self):
        num = self.total_day * self.timebins_per_day
        day_count = 1
        for j in range(1, num + 1):
            c_matrix = []
            for filename1 in self.C_path_list:
                for filename2 in self.C_path_list:
                    raw_data1 = pd.read_csv(filename1, names=['date', 'value'])
                    raw_data2 = pd.read_csv(filename2, names=['date', 'value'])

                    raw_data1['date'] = pd.to_datetime(raw_data1['date'], unit='s')
                    raw_data2['date'] = pd.to_datetime(raw_data2['date'], unit='s')
                    raw_data1 = raw_data1.sort_values(by=['date'])
                    raw_data2 = raw_data2.sort_values(by=['date'])
                    imfs1 = emd(np.array(raw_data1))
                    imfs2 = emd(np.array(raw_data2))

                    c_matrix.append(bind(imfs1, imfs2, self.fs, self.frequency_range, self.timebins_per_day, self.total_day)
                                    .getCmatrix(j))
            self.C = np.array(c_matrix).reshape((self.d, self.d))
            df = pd.DataFrame(self.C)
            file_name = 'C_day' + str(day_count) + '_range' + str(self.frequency_range) + '_timebin' \
                        + str((j - 1) % self.timebins_per_day) + '.csv'
            df.to_csv(self.C_output_path + file_name)
            day_count = day_count + j / self.timebins_per_day

    def anomaly_detector(self, sensor_id, tao, p, b, start_day, end_day):
        search_object = search(self.R, self.R_output_path, self.C_output_path, self.timebins_per_day, tao, p, b)
        anomalies_list = []
        C_list = search_object.get_Cmatrix_list(start_day, end_day)
        l_list = []
        for cmatrix in C_list:
            l_list.append(search_object.behavior_change(cmatrix, sensor_id))
        MAD = search_object.MAD(l_list, b)
        for t in range(len(l_list)):
            anomalies_list.append(search_object.anomaly(l_list, MAD, t))
        return anomalies_list










