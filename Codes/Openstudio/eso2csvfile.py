import esoreader
import pandas as pd
import matplotlib.pyplot as plt

ESO_path = "/Users/wuxiaodong/Dropbox/adaptive-anomalies/demo/eso/"
CSV_path = "/Users/wuxiaodong/Dropbox/adaptive-anomalies/demo/csv/"


def eso2csv(subpath, variable):
    eso = esoreader.read_from_path(ESO_path + subpath)
    time_index = pd.date_range('2009-01-01', periods=1152, freq='10min')  # 10 mins for each timestamp
    df = eso.to_frame(variable, index=time_index)
    sensor_list = df.columns.values.tolist()
    #for sensor in sensor_list:
    sensor = sensor_list[0]
    df[sensor].to_csv(CSV_path + variable + '_' + sensor + '.csv')


variables = ['Lights Electric Energy', 'Electric Equipment Electric Energy', 'Zone Total Internal Total Heating Energy',
             'Zone Air Temperature', 'People Occupant Count']


for variable in variables:
    if variable == 'Lights Electric Energy':
        eso2csv('eplusout.eso', variable)
