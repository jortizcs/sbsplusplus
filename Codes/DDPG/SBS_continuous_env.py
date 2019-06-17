import gym
from gym import spaces
import numpy as np
import reward_function

class SBS_continuous_env(object):
    metadata = {'render.modes': []}
    dt = .1  # refresh rate
    action_bound = [0, 10]
    # state_dim = 2
    # action_dim = 2
    state_dim = 2 * 30
    action_dim = 2 * 30

    def __init__(self):
        self.sbs_info = np.zeros(
            2*30, dtype=[('thresholds', np.float32)])
        self.sensor = np.arange(0, 30)
        self.sbs_info['thresholds'] = 1.  # 3 thresholds information
        #self.tar_r = 0
        self.tar_F1 = 0.
        self.ground_truth = reward_function.ground_truth_interface(self.sensor)

    def step(self, action):
        done = False
        r = 0.

        self.sbs_info['thresholds'] += action * self.dt
        self.sbs_info['thresholds'] %= 10  # normalize

        #if self.sbs_info['thresholds'][1] < 1.:
            #self.sbs_info['thresholds'][1] = 1.     # p must be larger or equal to 1

        # state
        s = self.sbs_info['thresholds']

        #(tao, b) = self.sbs_info['thresholds']  # thresholds

        #(tp, fn, fp, tn) = reward_function.ground_truth_check_multi(self.sbs_info['sensor'][0], [tao, b])
        (tp, fn, fp, tn) = reward_function.ground_truth_check_multi(self.sensor, self.sbs_info['thresholds'], self.ground_truth)

        if np.sum(tp) == 0 and np.sum(fn) == 0:
            recall = 1.
        elif np.sum(tp) == 0 and np.sum(fp) == 0:
            precision = 1.
        else:
            recall = np.sum(tp) / (np.sum(tp) + np.sum(fn) + 0.0)
            precision = np.sum(tp) / (np.sum(tp) + np.sum(fp) + 0.0)

        F1 = 2*(precision * recall) / (precision + recall)
        #cur_r = 5 * np.sum(tp) + -5 * np.sum(fn) + np.sum(tn) - np.sum(fp)
        #dis = self.tar_r - cur_r
        #r = -dis + 10
        #print (tp, fn, fp, tn)
        dis = self.tar_F1 - F1
        r = -dis
        if F1 > self.tar_F1:
            #print (tp, fn, fp, tn)
            f = open('/home/ec2-user/sbsplusplus/flip_6hours_3_DDPG_f1.txt', 'a')
            f.write('\n')
            f.write(str(tp))
            f.write('\n')
            f.write(str(fn))
            f.write('\n')
            f.write(str(fp))
            f.write('\n')
            f.write(str(tn))
            f.write('\n')
            f.write('F1 score: '+str(F1))
            f.write('\n')
            f.write('recall: '+str(recall))
            f.write('\n')
            f.write('precision: '+str(precision))
            f.write('\n')
            done = True
            r = 10.
            self.tar_F1 = F1
            # if self.tar_r < 36*30:
            #     self.tar_r = cur_r
            # else:
            #     self.tar_r = 36*30
            # f.write("target change to: " + str(self.tar_r)+'\n')

        return s, r, done

    def reset(self):
        self.sbs_info['thresholds'] = np.random.rand(2*30) * 10
        return self.sbs_info['thresholds']

    def render(self):
        return None

    def sample_action(self):
        return np.random.rand(8)*10  # three thresholds


if __name__ == '__main__':
    env = SBS_continuous_env()
    while True:
        env.step(env.sample_action())
        print env.sbs_info
