from RL_brain import DeepQNetwork
from SBS_env import SBS_env
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np


def run(sensor):
    # set evn
    env = SBS_env(sensor)
    env = env.unwrapped

    print(env.action_space)
    print(env.observation_space)
    print(env.observation_space.high)
    print(env.observation_space.low)

    # set RL method
    RL = DeepQNetwork(n_actions=env.action_space.n,
                      n_features=env.observation_space.shape[0],
                      learning_rate=0.01, e_greedy=0.9,
                      replace_target_iter=100, memory_size=2000,
                      e_greedy_increment=0.001,)

    total_steps = 0
    steps = []
    # start training
    for i_episode in range(100):

        observation = env.reset()
        ep_r = 0
        step = 0
        while True:
            step = step + 1
            env.render()    # show in graph

            action = RL.choose_action(observation)  # choose an action

            observation_, reward, done, info = env.step(action)     # observation from env

            benchmark, tao, p, b = observation_      # next state

            RL.store_transition(observation, action, reward, observation_)      # store them into memory: off policy
            print reward
            ep_r += reward
            if total_steps > 1000:      # store some memory before learning
                RL.learn()

            if done:
                steps.append(step)
                print('episode: ', i_episode,
                      'ep_r: ', round(ep_r, 2),
                      ' epsilon: ', round(RL.epsilon, 2))
                print observation
                break

            observation = observation_
            total_steps += 1

    #RL.plot_cost()
    return steps


s0 = run(1)
# tf.reset_default_graph()
# s1 = run(1)
# tf.reset_default_graph()
# s2 = run(2)

plt.plot(np.arange(len(s0)), s0, color='green', label='sensor0')
# plt.plot(np.arange(len(s1)), s1, color='red', label='sensor1')
# plt.plot(np.arange(len(s2)), s2, color='skyblue', label='sensor2')
# plt.legend()

plt.ylabel('Step')
plt.xlabel('Episode')
plt.show()
