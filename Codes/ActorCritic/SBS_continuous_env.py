import gym
from gym import spaces
import numpy as np
import reward_function


class SBS_continuous_env(object):
    metadata = {'render.modes': []}
    dt = .1  # refresh rate
    action_bound = [0, 10]
    state_dim = 3
    action_dim = 3

    def __init__(self):
        self.sbs_info = np.zeros(
            3, dtype=[('sensor', int), ('thresholds', np.float32)])
        self.sbs_info['sensor'] = 22
        self.sbs_info['thresholds'] = 1.  # 3 thresholds information

    def step(self, action):
        done = False
        r = 0.

        self.sbs_info['thresholds'] += action * self.dt
        self.sbs_info['thresholds'] %= 10  # normalize

        if self.sbs_info['thresholds'][1] < 1.:
            self.sbs_info['thresholds'][1] += 1.     # p must be larger or equal to 1

        # state
        s = self.sbs_info['thresholds']

        (tao, p, b) = self.sbs_info['thresholds']  # thresholds

        (tp, fn, fp, tn) = reward_function.ground_truth_check_yahoo(self.sbs_info['sensor'][0], [tao, p, b])
        r = 5 * tp + -5 * fn + tn - fp
        print (tp, fn, fp, tn)
        if r > 15:
            done = True
        return s, r, done

    def reset(self):
        self.sbs_info['thresholds'] = np.random.rand(3) * 10
        return self.sbs_info['thresholds']

    def render(self):
        return None

    def sample_action(self):
        return np.random.rand(3)*10  # three thresholds


if __name__ == '__main__':
    env = SBS_continuous_env()
    while True:
        env.step(env.sample_action())
        print env.sbs_info

