import numpy as np 
import matplotlib.pyplot as plt
import scipy.signal as signal
import pandas as pd

from scipy.interpolate import interp1d
from scipy.signal import hilbert, chirp
from scipy import interpolate


def findpeaks(x):
    index = signal.argrelextrema(x,np.greater)[0]
    return index

def getspline(x):


    N = np.size(x)
    peaks = findpeaks(x)
    peaks = np.concatenate(([0], peaks))
    peaks = np.concatenate((peaks, [N - 1]))
    if (len(peaks) <= 3):
        t = interpolate.splrep(peaks, y=x[peaks], w=None, xb=None, xe=None, k=len(peaks) - 1)
        return interpolate.splev(np.arange(N), t)
    t = interpolate.splrep(peaks, y=x[peaks])
    return interpolate.splev(np.arange(N), t)


def isMonotonic(x):
    maximas=findpeaks(x)
    minimas=findpeaks(-1*x)
    if (len(maximas) == 0)or(len(minimas) == 0):
        return True
    else:
        return False
    
def isImf(x):
    N = np.size(x)
    pass_zero = np.sum(x[0:N-2]*x[1:N-1]<0)
    peaks_num = np.size(findpeaks(x))+np.size(findpeaks(-x))
    if abs(pass_zero - peaks_num)>1:
        return False
    else:
        return True
    
def emd(x):
    imf = []
    while not isMonotonic(x):
        x1 = x
        while (not isImf(x1)):
            s1 = getspline(x1)          # upper envelope
            s2 = -getspline(-1*x1)      # lower envelope
            x2 = x1-(s1+s2)/2             # mean envelope
            x1 = x2
        imf.append(x1)
        x = x-x1
    imf.append(x)
    print imf
    return imf

def getFrequency(signal):
    fs = 400.0
    analytic_signal = hilbert(signal)
    amplitude_envelope = np.abs(analytic_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) / (2.0*np.pi) * fs)
    return instantaneous_frequency

def dataProcessing():
    raw_data = pd.read_csv('/Users/wuxiaodong/Desktop/18fall/SpecialProblem/Zone_Temp_RMI104.csv', names=['date', 'value'])
    #2_Mag_HW_Return_Temp   2_Mag_CHW_Supply_Temp   Zone_Temp_RMI104
    raw_data['date'] = pd.to_datetime(raw_data['date'], unit='s')
    raw_data = raw_data.sort_values(by=['date'])
    #plt.plot(raw_data['date'], raw_data['value'])
    #plt.show()
    return raw_data.values

if __name__ == '__main__':

    test = np.array([0.109017283,0.923722444,1.651182239,2.020828578,1.799564813,1.422650123,0.662718505,0.330908056,0.147316657,0.396244021,0.453235051,0.916266988,1.053167851,0.63681763,0.532051493,0.08994018,-0.717732329,-0.855063616,-0.680475165,0.071406017,0.913073764,1.855207585,2.682944133,2.667465224,2.479280179,1.992408687,1.348050833,0.994006146,0.822142278,0.591994742,0.886954149,1.260592311,1.230028317,1.217631396,0.644643686,-0.135081116,-0.711964767,-1.064944545,-0.777929926,-0.146634022,0.601942369,1.625442452,2.087659234,2.174841679,1.944062547,1.418676464,0.57214484,0.036795538,-0.000609289,-0.26336984,0.094634086,0.297793896,0.396835119,0.007259407,-0.858480906,-1.394269789,-1.85579278,-2.160075311,-1.824350703,-1.291997551,-0.538101879,0.267661313,0.699446876,1.217420847,0.781731188,0.036382748,-0.437728422,-1.00805078,-1.325132926,-1.159238528,-1.021807838,-0.824617407,-0.79444614,-0.886456075,-1.424007393,-1.955984975,-2.68713261,-2.773011756,-2.671641565,-1.684411326,-0.962753773,0.089646659,0.683509031,0.974626316,0.57909196,0.316738557,-0.261988737,-1.078689298,-1.06546717,-0.981400467,-0.572131872,-0.342081116,-0.090577818,-0.224030397,-0.706924146,-1.320851645,-1.916472444,-1.941698461,-1.716268291,-1.087495455,-0.005622723,0.938624738,1.683385158,2.046688054,1.845156075,1.439595372,0.658465234,0.197282301,0.108990311,0.395379929,0.71815339,0.90361103,0.988130991,0.718943517,0.474426139,-0.188698577,-0.812292702,-0.917224647,-0.816960237,0.075973199,0.93365717,2.02850965,2.385186217,2.84923888,2.551232478,2.008260359,1.432964394,0.969423566,0.511909795,0.821705124,0.830056202,1.101133254,1.200842308,1.09199242,0.374060592,-0.157511494,-0.727140266,-1.015692864,-0.798837593,-0.376662826,0.688543921,1.44398107,2.093600529,2.087501624,1.912169477,1.396776932,0.713375255,0.036906952,-0.423291188,-0.325659809,0.021862763])
    matrix = dataProcessing()
    #IMFs = emd(test)
    IMFs = emd(matrix[:,1])
    print len(IMFs)
    plt.plot(IMFs[1])
    plt.show()

