import gym


env = gym.make("MountainCar-v0")
env.reset()

print(env.observation_space.high)
print(env.observation_space.low)
print(env.action_space.n)

DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
discrete_os_win_size = (env.observation_space.high- env.observation_space.low)/DISCRETE_OS_SIZE
print(discrete_os_win_size)

done= False

while not done:
    action = 2
    new_state, reward, done, _,_ = env.step(action)
    env.render()

env.close()


