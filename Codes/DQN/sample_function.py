import numpy as np
import reward_function


dt = 0.1


# change tao, p and b according to action
def threshold_change(sensor, tao, p, b, action):
    a1, a2, a3 = ten_to_three(action)
    if a1 == 0:
        tao = tao
        if a2 == 0:
            p = p
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += dt
            else:
                b -= dt
                if b < 0:
                    b = 0.0
        elif a2 == 1:
            p += dt
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += dt
            else:
                b -= dt
                if b < 0:
                    b = 0.0
        else:
            p -= dt
            if p < 1.0:
                p = 1.0
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += dt
            else:
                b -= dt
                if b < 0:
                    b = 0.0
    elif a1 == 1:
        tao += dt
        if a2 == 0:
            p = p
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += dt
            else:
                b -= dt
                if b < 0:
                    b = 0.0
        elif a2 == 1:
            p += dt
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += dt
            else:
                b -= dt
                if b < 0:
                    b = 0.0
        else:
            p -= dt
            if p < 1.0:
                p = 1.0
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += dt
            else:
                b -= dt
                if b < 0:
                    b = 0.0
    else:
        tao -= dt
        if tao < 0.0:
            tao = 0.0
        if a2 == 0:
            p = p
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += dt
            else:
                b -= dt
                if b < 0:
                    b = 0.0
        elif a2 == 1:
            p += dt
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += dt
            else:
                b -= dt
                if b < 0:
                    b = 0.0
        else:
            p -= dt
            if p < 1.0:
                p = 1.0
            if a3 == 0:
                b = b
            elif a3 == 1:
                b += dt
            else:
                b -= dt
                if b < 0:
                    b = 0.0
    print tao, p, b
    return benchmark(sensor, tao, p, b), tao, p, b


# fool function of accuracy with thresholds
def accuracy(tao, p, b):
    return reward_function.ground_truth_check(0, [tao, p, b])


def benchmark(sensor, tao, p, b):
    tp, fn, fp, tn = reward_function.ground_truth_check(sensor, [tao, p, b])
    return 5 * tp + -5 * fn + tn - fp


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
