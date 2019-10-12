from Codes.strip_bind_search.SBS import SBS

R_PATH = '/Users/wuxiaodong/Dropbox/adaptive-anomalies/energyplus/normal/csv/'
C_PATH = '/Users/wuxiaodong/Dropbox/adaptive-anomalies/energyplus/anomaly/csv/'
FS = 0.0011     # sample frequency
FREQUENCY_RANGE = 1
TIMEBINS_PER_DAY = 4
TOTAL_DAY = 8
R_OUTPUT_PATH = '/Users/wuxiaodong/Dropbox/adaptive-anomalies/energyplus/normal/R/'
C_OUTPUT_PATH = '/Users/wuxiaodong/Dropbox/adaptive-anomalies/energyplus/anomaly/C/'


sbs = SBS(R_PATH, C_PATH, FS, FREQUENCY_RANGE, TIMEBINS_PER_DAY, TOTAL_DAY, R_OUTPUT_PATH, C_OUTPUT_PATH)

sbs.R_generator()
#sbs.C_generator()
#for s in range(0, 15):
    #sbs.anomaly_detector(s, 9, 4, 1.4826, 1, 8)

