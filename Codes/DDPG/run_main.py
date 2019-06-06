"""
Plug a RL method to the framework, this method can be discrete or continuous.
This script is based on a continuous action RL. If you want to change to discrete RL like DQN,
please change the env.py and rl.py correspondingly.
"""
from SBS_continuous_env import SBS_continuous_env
from RL_brain import DDPG

MAX_EPISODES = 30
MAX_EP_STEPS = 200
ON_TRAIN = True

# set env
env = SBS_continuous_env()
s_dim = env.state_dim
a_dim = env.action_dim
a_bound = env.action_bound

# set RL method (continuous)
rl = DDPG(a_dim, s_dim, a_bound)


def train():
    # start training
    reward = []
    max_reward = -36
    step = []
    for i in range(MAX_EPISODES):
        s = env.reset()
        ep_r = 0.
        for j in range(MAX_EP_STEPS):
            env.render()

            a = rl.choose_action(s)
            #print 'state: ', s
            #print 'action: ', a

            s_, r, done = env.step(a)
            #print 'reward: ', r
            if r > max_reward:
                max_reward = r
            reward.append(r)
            rl.store_transition(s, a, r, s_)

            ep_r += r
            if rl.memory_full:
                # start to learn once has fulfilled the memory
                rl.learn()
            s = s_
            if done or j == MAX_EP_STEPS-1:
                step.append(j)
                print('Ep: %i | %s | ep_r: %.1f | steps: %i' % (i, '---' if not done else 'done', ep_r, j))
                break
    rl.save()
    print 'Max Reward: '+ str(max_reward)
    import matplotlib.pyplot as plt
    import numpy as np
    plt.plot(np.arange(len(step)), step)
    plt.ylabel('Step')
    plt.xlabel('Episode')
    plt.show()


def eval():
    rl.restore()
    env.render()
    steps = []
    #env.viewer.set_vsync(True)
    reward = []
    for i in range(200):
        s = env.reset()
        for step in range(200):
            env.render()
            a = rl.choose_action(s)
            s, r, done = env.step(a)
            print r

            if done:
                steps.append(step)
                break
    import matplotlib.pyplot as plt
    import numpy as np
    plt.plot(np.arange(len(steps)), steps)
    plt.ylabel('Step')
    plt.xlabel('Episode')
    plt.show()



if ON_TRAIN:
    train()
else:
    eval()