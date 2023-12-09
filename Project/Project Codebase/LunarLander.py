from __future__ import print_function
from __future__ import division
import numpy as np
import gym
from gym import wrappers
import time
import random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from collections import deque

# -*- coding: utf-8 -*-
"""Harshita_Arya_CHW3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xPxVmIZ091ysWy_mvkaL18R7WgIP_d3W
"""

# pip install gym==0.25.2

# !pip install box2d-py==2.3.5
# !pip install pygame==2.1.0

"""Cart Pole
===
In this assignment we implement DQN method for the cart pole problem.

Problem Description
---
This environment corresponds to the version of the cart-pole problem described by Barto, Sutton, and Anderson in “Neuronlike Adaptive Elements That Can Solve Difficult Learning Control Problem”. A pole is attached by an un-actuated joint to a cart, which moves along a frictionless track. The pendulum is placed upright on the cart and the goal is to balance the pole by applying forces in the left and right direction on the cart. For more information please visit https://www.gymlibrary.dev/environments/classic_control/cart_pole/.

Your Job
---
1. Read https://www.gymlibrary.dev/environments/classic_control/cart_pole/ to understand the environment, states, reward function, etc.
2. Implement the DQN method.
3. Answer the questions in a pdf.
4. Some helpful API documentation can be found here: https://www.gymlibrary.dev/api/core/.
"""



"""We use environment 'CartPole-v1'. Run the following cell to test the environment."""

## A demo of operating in this environment with a random policy

# def run_random_policy(env, gamma, render = False):
#     """
#     Run 15 episodes by taking random actions.
#     args:
#     env: gym environment.
#     gamma: discount factor.
#     render: boolean to turn rendering on/off.
#     """
#     obs = env.reset()
#     for i in range(15):
#         step_idx = 0
#         total_reward = 0
#         env.reset()
#         while True:
#             if render:
#                 env.render()
#             #choose an action randomly.
#             #env.step() returns a tuple (state, reward, done) where done is a boolen indicater for episode endings.
#             obs, reward, done , _ ,_= env.step(env.action_space.sample())
#             total_reward += (gamma ** step_idx * reward)
#             step_idx += 1
#             if done:
#                 break

# env_name  = 'LunarLanderContinuous-v2'
# env = gym.make(env_name).unwrapped
# # Get the action space and observation space
# action_space = env.action_space
# observation_space = env.observation_space

# print("Action space:")
# print("Type:", action_space)
# print("Shape:", action_space.shape)  # For continuous spaces, this might not be defined
# print("High:", action_space.high)    # Maximum values for each action dimension
# print("Low:", action_space.low)      # Minimum values for each action dimension

# print("\nObservation space:")
# print("Type:", observation_space)
# print("Shape:", observation_space.shape)  # Shape of the state/observation space
# print("High:", observation_space.high)    # Maximum possible values for each observation dimension
# print("Low:", observation_space.low) 
# run_random_policy(env, gamma=0.99, render = True)
# env.close()

class BetaSampleBufferClass():
    def __init__(self,  batch_size=32, size=1000000):
        self.batch_size = batch_size
        self.memory = deque(maxlen=size)  # Your data buffer

    def remember(self, s_t, a_t, r_t, s_t_next, d_t):
        '''
        s_t (np.ndarray double): state
        a_t (np.ndarray int): action
        r_t (np.ndarray double): reward
        d_t (np.ndarray float): done flag
        s_t_next (np.ndarray double): next state
        '''
        self.memory.append((s_t, a_t, r_t, s_t_next, d_t))

    def sample(self):
        '''
        Random sampling of data from the buffer
        '''
        size = min(self.batch_size, len(self.memory))

        # Define parameters for the Beta distribution
        alpha = 2  # Modify as needed
        beta = 5   # Modify as needed

        # Generate samples based on the Beta distribution
        # Ensure the values are within the range [0, len(self.memory)]
        indexes = np.random.beta(alpha, beta, size) * len(self.memory)
        indexes = np.floor(indexes).astype(int)

        # Retrieve samples based on the generated indexes
        samples = [self.memory[i] for i in indexes]

        return samples

class DQN(nn.Module):
     #Input: state
     #Output: vector corresponding to state-action values for actions, i.e. Q(s,a).
    def __init__(self):
        super(DQN, self).__init__()

        ########################### Your Code Here ###########################

        'Define a neural network that takes state as an input and outputs Q(s,a) for each actions.'
        'You should use ONLY 1 hidden layer with say 50 hidden nodes and ReLU activation function'
        n_observation = env.observation_space
        n_action = env.action_space
        self.layer1 = nn.Linear(n_observation.shape[0],50)
        self.layer2 = nn.Linear(50,n_action.shape[0])

        ########################### Your Code Here ###########################

    def forward(self, x):
        ########################### Your Code Here ###########################

        'Define the forward method to get output from your neural network for a given state x as input and return this output'
        x= torch.as_tensor(x).float()
        x= F.relu(self.layer1(x))
        return self.layer2(x)

        ########################### Your Code Here ###########################


def choose_action(model, state, EPSILON = 0.9):
    """
    This is the epsilon-greedy strategy.
    """

    ########################### Your Code Here ###########################
    # print("In Choose Action")

    'Write an epsilon greedy strategy to choose action based upon Q(s,a) calculated through your model'
    'Return the action'
    if np.random.rand() > EPSILON:
        #   print(env.action_space.sample(),"there")
        return env.action_space.sample()
    else:
        with torch.no_grad():
            # print(model(state).numpy(),"here")
            return model(state).numpy()

    ########################### Your Code Here ###########################

def copy_parameters(local_model, target_model):
    """
    Update model parameters.
    local model (PyTorch model): weights will be copied from.
    target model (PyTorch model): weights will be copied to.
    """
    for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
        target_param.data.copy_(local_param.data)

def plot_returns(returns, x, title):
    '''
    Returns (iterable): list of returns over time
    window: window for rolling mean to smooth plotted curve
    '''
    plt.figure(figsize=(8, 6))  # Adjust figure size if needed
    sns.lineplot(
        data=pd.DataFrame(returns),color=x
    )
    plt.title(title)
    plt.xlabel('Epoch')
    plt.ylabel('Reward')
    plt.show()

def DQN_update(model, model_ft, gamma, epochs, render = False):
    """
    Use online learning to update DQN.
    args:
    model (DQN): DQN model
    model_ft (DQN): DQN model for fixed target
    """
    reward_history = []
    initial_reward= []
    optimizer = torch.optim.Adam(model.parameters(), lr = 0.001) #feel free to tweak the learning rate

    replay_buffer = BetaSampleBufferClass(batch_size=1)

    #run epoches of episodes
    #stop at done or 10k epochs

    for i in range(epochs):
        print(i)
        state = env.reset()   #reset enviroment. Get initial state.
        total_reward = 0
        total_reward1 = 0

        if i%100 == 0: #update the fixed target network parameters every 100 epochs.
            copy_parameters(model, model_ft)


        ########################### Your Code Here ###########################

        for t in range(5000):
          action = choose_action(model,state)
          next_state, reward, done, _,_ = env.step(action)

          replay_buffer.remember(state, action, reward, next_state, done)
          state = next_state

          for batch in replay_buffer.sample():
            s_t = torch.as_tensor(batch[0]).double()
            a_t = torch.as_tensor(batch[1]).long()
            r_t = torch.as_tensor(batch[2]).double()
            s_t_next = torch.as_tensor(batch[3]).double()
            d_t = torch.as_tensor(batch[4]).double()

            total_reward+=r_t
            q_ft= r_t+gamma*torch.max(model_ft(s_t_next), dim=0)[0]
            criterion = nn.SmoothL1Loss()(torch.max(model(s_t), dim=0)[0].unsqueeze(0).unsqueeze(0), q_ft.unsqueeze(0).unsqueeze(0))



        reward_history.append(torch.tensor(total_reward).item())
        initial_reward.append(total_reward1)

    plot_returns(reward_history,"red","Lunar Lander Rewards")
        ########################### Your Code Here ###########################

if __name__ == '__main__':
    gamma = 0.99
    np.random.seed(1111)
    # env = gym.make("LunarLander-v2",continuous: bool = False, gravity: float = -10.0, enable_wind: bool = False, wind_power: float = 15.0, turbulence_power: float = 1.5,).unwrapped
    env = gym.make('LunarLanderContinuous-v2').unwrapped
    model = DQN()
    model_ft = DQN()
    DQN_update(model, model_ft, gamma = 0.99, epochs = 4000, render = True) #Try different epochs until convergence.
    env.close()

    ## Write any other lines of code if you need it for plotting and other purposes.