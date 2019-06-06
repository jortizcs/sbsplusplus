import gym
from gym import spaces
import numpy as np
import reward_function


class SBS_continuous_env(object):
    metadata = {'render.modes': []}
    dt = .1  # refresh rate
    action_bound = [0, 10]
    state_dim = 2
    action_dim = 2

    def __init__(self):
        self.sbs_info = np.zeros(
            2, dtype=[('sensor', int), ('thresholds', np.float32)])
        self.sbs_info['sensor'] = 3
        self.sbs_info['thresholds'] = 1.  # 3 thresholds information
        self.tar_r = 35


    def step(self, action):
        done = False
        r = 0.

        self.sbs_info['thresholds'] += action * self.dt
        self.sbs_info['thresholds'] %= 10  # normalize

        #if self.sbs_info['thresholds'][1] < 1.:
            #self.sbs_info['thresholds'][1] = 1.     # p must be larger or equal to 1

        # state
        s = self.sbs_info['thresholds']

        (tao, b) = self.sbs_info['thresholds']  # thresholds

        (tp, fn, fp, tn) = reward_function.ground_truth_check(self.sbs_info['sensor'][0], [tao, b])
        cur_r = 5 * tp + -5 * fn + tn - fp
        dis = abs(self.tar_r - cur_r)
        r = -dis + 10
        print (tp, fn, fp, tn)
        if cur_r > self.tar_r:
            done = True
            if self.tar_r < 35:
                self.tar_r = cur_r
            else:
                self.tar_r = 35
            print "target change to: "+ str(self.tar_r)
        return s, r, done

    def reset(self):
        self.sbs_info['thresholds'] = np.random.rand(2) * 10
        return self.sbs_info['thresholds']

    def render(self):
        return None

    def sample_action(self):
        return np.random.rand(2)*10  # three thresholds


if __name__ == '__main__':
    env = SBS_continuous_env()
    while True:
        env.step(env.sample_action())
        print env.sbs_info
