import numpy as np

result = [[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1], [1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 0, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 1], [0, 4, 1, 2, 1, 2, 5, 1, 2, 2, 4, 2, 3, 1, 4, 0, 2, 5, 2, 0, 3, 0, 5, 0, 1, 1, 3, 3, 0, 6], [22, 18, 21, 20, 21, 20, 17, 21, 20, 20, 18, 20, 19, 21, 18, 22, 20, 17, 20, 22, 19, 22, 17, 22, 21, 21, 19, 19, 22, 16]]

tp = result[0]
fn = result[1]
fp = result[2]
tn = result[3]


recall = []
precision = []
for i in range(30):
    if (tp[i]+fn[i]+0.0) != 0:
        recall.append(tp[i]/(tp[i]+fn[i]+0.0))
    if (tp[i] + fp[i] + 0.0) != 0:
        precision.append(tp[i]/(tp[i]+fp[i]+0.0))
print np.mean(recall)
print np.mean(precision)
print np.var(recall)
print np.var(precision)
print np.std(recall)
print np.std(precision)
print recall
print precision



