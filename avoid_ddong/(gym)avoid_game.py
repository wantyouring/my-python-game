# gym interface.

import gym
import numpy as np
from gym import spaces
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq import CnnPolicy
from stable_baselines import DQN


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(CustomEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(3)
        # Example for using image as input:
        #self.observation_space = spaces.Box(low=0, high=255, shape=(64, 48, 1), dtype=np.uint8)
        self.observation_space = spaces.Box(low=0, high=255, shape=(64, 48, 1))
        self.reset()

    def step(self, action):
        self.step_cnt += 1
        reward = 1
        done = False

        if action == 1:
            self.man_x -= self.man_speed
        elif action == 2:
            self.man_x += self.man_speed

        # move man
        if self.man_x < 0:
            self.man_x = 0
        elif self.man_x > 44:
            self.man_x = 44

        # move ddong
        for index, value in enumerate(self.ddong_y):
            self.ddong_y[index] += self.ddong_speed
            if value > 64:
                self.ddong_y[index] = -4

        # check done
        for index, value in enumerate(self.ddong_y):
            if abs(self.ddong_x[index] - self.man_x) < 4 and self.man_y - self.ddong_y[index] <  4:
                done = True
                reward = -1 # penalty when the game end
        state = self.return_state()
        return state, reward, done, {}

    def reset(self):
        self.ddong_x, self.ddong_y = [], []
        fixed_ddong_x = [8, 7, 4, 2, 5, 9, 0, 1, 3, 6]
        fixed_ddong_y = [8, 10, 8, 1, 0, 0, 17, 12, 1, 5]
        for i in range(10):
            self.ddong_x.append(int(fixed_ddong_x[i] * 4.8))
            self.ddong_y.append(int(fixed_ddong_y[i] * -3.2))
        self.man_x = 0
        self.man_y = int(64 * 0.9)
        self.ddong_speed = 4
        self.man_speed = 4
        self.step_cnt = 0

    def render(self, mode='human', close=False):
        # check
        print("step : {}".format(self.step_cnt))

    def return_state(self):
        state = [[0] * 48 for _ in range(64)]

        for i in range(10):
            for j in range(4):
                for k in range(4):
                    if self.ddong_y[i] >= 0 and self.ddong_y[i] + j < 64:
                        state[self.ddong_y[i] + j][self.ddong_x[i] + k] = 255

        for i in range(4):
            for j in range(4):
                state[self.man_y + i][self.man_x + j] = 180
        return np.reshape(state, (64, 48, 1))

# Instantiate and wrap the env
env = DummyVecEnv([lambda: CustomEnv()])
# Define and Train the agent
model = DQN(CnnPolicy, env,verbose=1)
#model = DQN.load("model_saved") # continued from 30000 learned model
model.learn(total_timesteps=100000)
model.save("model_saved")
'''
# test model
state = env.reset()
while True:
    action, next_state = model.predict(state)
    state, reward, done, info = env.step(action)
    env.render()
'''
