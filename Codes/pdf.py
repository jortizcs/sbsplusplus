import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import norm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import seaborn as sns
import os
import search

path = '/Users/wuxiaodong/Dropbox/adaptive-anomalies/C/range1/'
path_R = '/Users/wuxiaodong/Dropbox/adaptive-anomalies/R/3day/R_Rice_3_day_range1.csv'
d = 20
# constant b of MAD:
b = 1.4826


def corr_list(s1, s2):
    correlations = []
    path_list = os.listdir(path)
    for csv in path_list:
        csv_path = path + csv
        df = pd.read_csv(csv_path)
        C = df.values[:, 1:]    # remove the first unnamed column in C csv files
        correlations.append(C[s1, s2])
    return correlations


def variance(s1, s2):
    correlations = corr_list(s1, s2)
    return np.var(correlations)


def variance_list(d):
    list = []
    for i in range(0, d):
        print i
        for j in range(i, d):
            list.append(variance(i, j))
    print list
    return list


def pdf(s1, s2):
    arr = corr_list(s1, s2)
    print arr

    # plot histogram
    plt.hist(arr, 24)
    plt.axis([-2, 2, 0, 5])

    # get the normal distribution
    (mu, sigma) = norm.fit(arr)
    print "mu: "+str(mu)
    print "sigma: "+str(sigma)

    # plot the fitted model
    x = np.linspace(-2, 2, 100)
    y = mlab.normpdf(x, mu, sigma)
    plt.plot(x, y)

    # standard deviation
    plt.fill_between(x, y, where = (x > mu + sigma), facecolor='red')
    plt.fill_between(x, y, where=(x < mu - sigma), facecolor='red')
    #
    df = pd.read_csv(path_R)
    R = df.values[:, 1:]  # remove the first unnamed column in C csv file
    r_value = R[s1, s2]
    print "reference value: " + str(r_value)
    list = abs(arr-r_value)
    mad_value = search.MAD(list, b)
    threshold = 1
    t_line = np.median(list) + threshold * mad_value


    plt.vlines(t_line+r_value, 0, 5)
    plt.vlines(r_value-t_line, 0, 5)



def cdf(d):
    list = variance_list(d)
    counts, bin_edges = np.histogram(list)
    counts = counts.astype(float) / len(list)
    cdf = np.cumsum(counts)
    plt.plot(bin_edges[1:], cdf)

    plt.show()


if __name__ == '__main__':
    plt.subplot(221)
    pdf(1, 2)

    plt.subplot(222)
    pdf(28, 529)

    plt.subplot(223)
    pdf(52,44)

    plt.show()
