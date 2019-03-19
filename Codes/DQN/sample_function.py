import numpy as np


# change tao, p and b according to action
def threshold_change(tao, p, b, action):
    a1, a2, a3 = ten_to_three(action)
    if a1 == 0:
        tao = tao
        if a2 == 0:
            p = p
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += 0.1
            else:
                b -= 0.1
                if b < 0:
                    b = 0.0
        elif a2 == 1:
            p += 0.1
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += 0.1
            else:
                b -= 0.1
                if b < 0:
                    b = 0.0
        else:
            p -= 0.1
            if p < 0:
                p = 0.0
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += 0.1
            else:
                b -= 0.1
                if b < 0:
                    b = 0.0
    elif a1 == 1:
        tao += 0.1
        if a2 == 0:
            p = p
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += 0.1
            else:
                b -= 0.1
                if b < 0:
                    b = 0.0
        elif a2 == 1:
            p += 0.1
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += 0.1
            else:
                b -= 0.1
                if b < 0:
                    b = 0.0
        else:
            p -= 0.1
            if p < 0:
                p = 0.0
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += 0.1
            else:
                b -= 0.1
                if b < 0:
                    b = 0.0
    else:
        tao -= 0.1
        if a2 == 0:
            p = p
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += 0.1
            else:
                b -= 0.1
                if b < 0:
                    b = 0.0
        elif a2 == 1:
            p += 0.1
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += 0.1
            else:
                b -= 0.1
                if b < 0:
                    b = 0.0
        else:
            p -= 0.1
            if p < 0:
                p = 0.0
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += 0.1
            else:
                b -= 0.1
                if b < 0:
                    b = 0.0
    return accuracy(tao, p, b), tao, p, b


# fool function of accuracy with thresholds
def accuracy(tao, p, b):
    return abs(np.sin(tao*p + b))


# transform action to three specific actions: a1, a2, a3
def ten_to_three(x):
    a3 = x % 3
    x = x/3
    a2 = x % 3
    x = x/3
    a1 = x%3
    return a1, a2, a3


if __name__ == '__main__':
    print threshold_change(9,3,0, 26)
