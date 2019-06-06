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
    state_dim = 8
    action_dim = 8

    def __init__(self):
        self.sbs_info = np.zeros(
            8, dtype=[('thresholds', np.float32)])
        self.sensor = np.array([0,1,2,3])
        self.sbs_info['thresholds'] = 1.  # 3 thresholds information
        self.tar_r = 35

        self.sensor = np.array([0,1,2,3])
        self.sbs_info['thresholds'] = 1.  # 3 thresholds information
        self.tar_r = 0
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
        cur_r = 5 * np.sum(tp) + -5 * np.sum(fn) + np.sum(tn) - np.sum(fp)
        dis = abs(self.tar_r - cur_r)
        r = -dis + 10
        print (tp, fn, fp, tn)
        if cur_r > self.tar_r:
            done = True
            if self.tar_r < 35*4:
                self.tar_r = cur_r
            else:
                self.tar_r = 35*4
            print "target change to: " + str(self.tar_r)
        return s, r, done

    def reset(self):
        self.sbs_info['thresholds'] = np.random.rand(8) * 10
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
