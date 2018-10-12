import numpy as np 
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.stats as stats

from scipy.interpolate import interp1d
from scipy.signal import hilbert, chirp
'''
def aggregation(x):#to do
    for clusters in x:
        result = np.mean(clusters,axis=x)
'''
def correlation(x,y):
    return stats.pearsonr(x,y)[0] #get the cor of two signals

def getReference(s1,s2):
    n = 10 #number of time bins
    j = 0 #current time range
    
    #cut each IMF in s1:
    isolated1 = [[],[],[],[]]
    for j in range(4):
        for i in range(0,len(s1[j]),len(s1[j])/n): #devide IMFj into n parts
            isolated1[j].append(s1[j][i:i+len(s1[j]/n)])
            
    #cut each IMF in s2:
    isolated2 = [[],[],[],[]]
    for j in range(4):
        for i in range(0,len(s2[j]),len(s2[j])/n): 
            isolated2[j].append(s2[j][i:i+len(s2[j]/n)])
            
    #compute the correlations        
    matrix1 = np.array(isolated1)
    matrix2 = np.array(isolated2)
    matrixCor = np.zeros((n,4))
    for x in range(0,n):
        for y in range(0,4):
            matrixCor[x][y] = correlation(matrix1[x][y],matrix2[x][y])
            
    #get the median
    medianList = []
    for l in range(0,4):
        medianList.append(np.median(matrixCor[:,l])

    return medianList

def getCluster(IMFs):
    frequencies = []    #frequency of each IMFs
    for imf in IMFs:
        frequency = getFrequency(imf)
        frequencies.append(frequency)
        
    clusters = [[],[],[],[]]
                          
    #4 time scale ranges
    range1 = 20 * 60
    range2 = 6 * 60 * 60
    range3 = 6 * 60 * 60 * 24
    i = 0
    for f in frequencies:
        if f<range1:
            clusters[0].append(IMFs[i])
        elif f in range(range1,range2):
            clusters[1].append(IMFs[i])
        elif f in range(range2,range3):
            clusters[2].append(IMFs[i])
        elif f > range3:
            clusters[3].append(IMFs[i])
        i=i+1
    return clusters

def getReference2(matrix1,matrix2):#to do
    n = 10 #number of time bins
    l = len(matrix[:,0])
    matrixCol = [[]]
    for i in range(
    matrixCol[0].append(np.corrcoef(matrix1[:,0][0,l/i],matrix2[:,0][0,n]))
