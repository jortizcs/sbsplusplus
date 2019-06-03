import gym
from gym import spaces
import numpy as np
import sample_function


class SBS_env(gym.Env):
    metadata = {'render.modes': []}

    def __init__(self, sensor):
        self.sensor = sensor
        self.action_space = spaces.Discrete(27)
        '''
        p, b, tao each has 3 actions: 
            0: remain
            1: increase
            2: decrease
        
        '''
        self.observation_space = spaces.Box(low=np.array([0.0, 0.0, 1.0, 0.0]),
                                            high=np.array([20.0, 10.0, 10.0, 10.0]))
        '''
        state:  benchmark(0.0, 20.0)
                tao(0.0, 10.0)
                p(1.0, 10.0)
                b(0.0, 10.0)               
        '''
        self.state = None

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        benchmark, tao, p, b = self.state  # state is accuracy

        self.state = sample_function.threshold_change(self.sensor, tao, p, b, action)   # return state of SBS with current combination of thresholds
        self.counts += 1

        done = benchmark >= 35.0  # if accuracy exceeds 0.6, finish step
        done = bool(done)

        if not done:
            reward = -0.1   # every time take an action, reward decreases 0.1
        else:
            if benchmark >= 35.0:
                reward = 100     # once reach target, reward increases 10
            else:
                reward = -50    # if has not reached target after done, reward decreases 50

        return np.array(self.state), reward, done, {}  # return state, reward, done and info

    def reset(self):
        # randomly reset the initial thresholds over [0,1)
        tao = np.random.randint(0, 3)
        p = np.random.randint(1, 3)
        b = np.random.randint(0, 3)
        benchmark = sample_function.benchmark(self.sensor, tao, p, b)
        self.state = benchmark, tao, p, b
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
