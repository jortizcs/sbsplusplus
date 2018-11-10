import scipy.signal as signal
import pylab as pl
import numpy as np


if __name__ == '__main__':

    sampling_rate = 1/900 + 0.0

    # wp, ws
    # maximum loss dB
    # minimum attenuation dB
    b, a = signal.iirdesign([0.04, 0.75], [0.03, 0.8], 2, 40)





