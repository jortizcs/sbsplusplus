import gym
from gym import spaces
import numpy as np
import sample_function


class SBS_env(gym.Env):
    metadata = {'render.modes': []}

    def __init__(self):
        self.target = 1.0  # target accuracy of SBS
        self.action_space = spaces.Discrete(27)
        '''
        p, b, tao each has 3 actions: 
            0: remain
            1: increase
            2: decrease
        
        '''
        self.observation_space = spaces.Box(low=np.array([0.0, 0.0, 0.0, 0.0]),
                                            high=np.array([1.0, 10.0, 10.0, 10.0]))
        '''
        state:  accuracy(0.0, 1.0)
                tao(0.0, 10.0)
                b(0.0, 10.0)
                p(0.0, 10.0)               
        '''
        self.state = None

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        accuracy, tao, b, p = self.state  # state is accuracy

        # TODO: threshold_change(tao, b, p, action[0], action[1], action[2])

        self.state = sample_function.threshold_change(tao, p, b, action)   # return state of SBS with current combination of thresholds
        self.counts += 1

        done = accuracy >= 0.8  # if accuracy exceeds 0.8, finish step
        done = bool(done)

        if not done:
            reward = -0.1   # every time take an action, reward decreases 0.1
        else:
            if accuracy >= 0.8:
                reward = 10     # once reach target, reward increases 10
            else:
                reward = -50    # if has not reached target after done, reward decreases 50

        return np.array(self.state), reward, done, {}  # return state, reward, done and info

    def reset(self):
        thresholds = np.random.rand(3)    # randomly reset the initial thresholds over [0,1)
        accuracy = sample_function.accuracy(thresholds[0], thresholds[1], thresholds[2])
        self.state = sample_function.threshold_change(accuracy, thresholds[0], thresholds[1], thresholds[2])
        self.counts = 0
        return np.array(self.state)

    def render(self, mode='human'):
        return None

    def close(self):
        return None


if __name__ == '__main__':
    env = SBS_env
    env.reset()
    env.step(env.action_space.sample())
    print(env.state)
    env.step(env.action_space.sample())
    print(env.state)
