from RL_brain import DeepQNetwork
from SBS_env import SBS_env

# set evn
env = SBS_env()
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

# start training
for i_episode in range(100):

    observation = env.reset()
    ep_r = 0
    while True:
        env.render()    # show in graph

        action = RL.choose_action(observation)  # choose an action

        observation_, reward, done, info = env.step(action)     # observation from env

        accuracy, tao, b, p = observation_      # next state

        RL.store_transition(observation, action, reward, observation_)      # store them into memory: off policy

        ep_r += reward
        if total_steps > 1000:
            RL.learn()

        if done:
            print('episode: ', i_episode,
                  'ep_r: ', round(ep_r, 2),
                  ' epsilon: ', round(RL.epsilon, 2))
            print observation
            break

        observation = observation_
        total_steps += 1

RL.plot_cost()