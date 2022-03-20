from stable_baselines3 import PPO
from stable_baselines3 import A2C
from stable_baselines3 import DQN

import gym
from datetime import datetime
import numpy as np
from gym import spaces
from BreakoutGame import BreakoutGame
import GameObjects

class BreakoutAgent(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}
  
  # Action Constants
  LEFT = 0
  RIGHT = 1

  def __init__(self):
    super(BreakoutAgent, self).__init__()
    number_of_actions = 2
    number_of_observations = 4
    self.action_space = spaces.Discrete(number_of_actions)
    self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(number_of_observations,), dtype=np.float32)
    self.game = BreakoutGame()
    self.observer = GameObjects.Observer()
    self.prevScore = 0
    self.game.attach(self.observer)

  def step(self, action):
    self.game.runLogic(action)

    reward = 0
    done = (self.observer.event.lives == 0)
    info = {"score": self.observer.event.score, "lives": self.observer.event.lives}

    ball = self.observer.event.ball.rect
    bat = self.observer.event.bat.rect
    dif_l = abs(ball.left - bat.left)
    dif_r = abs(ball.right - bat.right)    

    if ball.top > 200 and (dif_l < 50 or dif_r < 50):
        reward = 1
    else:
        reward = -1

    if self.observer.event.score - self.prevScore > 0:
      reward = 100

    self.prevScore = self.observer.event.score
    return np.array([ball.left, ball.right, bat.left, bat.right], dtype=np.float32), reward, done, info

  def reset(self):
    self.game.initGame()
    ball = self.observer.event.ball.rect
    bat = self.observer.event.bat.rect
    return np.array([ball.left, ball.right, bat.left, bat.right], dtype=np.float32)

  def render(self, mode='human'):
    self.game.render()

if __name__=="__main__":

    list_algs = [PPO, A2C, DQN]
    list_algs_names = ["ppo", "a2c", "dqn"]
    list_steps = [10000, 50000, 100000, 500000, 1000000]
    #list_steps = [1, 10, 50, 100]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i in range(0, len(list_algs)):
      for j in range(0, len(list_steps)):
        filename = "_" + list_algs_names[i] + "_" + str(list_steps[j])

        env = BreakoutAgent()
        model = list_algs[i]('MlpPolicy', env, verbose=1)
        model.learn(total_timesteps=list_steps[j]) 
        obs = env.reset()
        model.save("models/model" + filename)

        for k in range(2000):
          action, _state = model.predict(obs, deterministic=True)
          obs, reward, done, info = env.step(action)
          env.render()
          print(info)
          if done:
            obs = env.reset()

        with open("scores/score_" + timestamp + ".csv", "a") as file:
          p1 = list_algs_names[i]
          p2 = str(list_steps[j])
          p3 = str(info["score"])
          p4 = str(info["lives"])
          p5 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          file.write(p1 + "," + p2 + "," + p3 + "," + p4 + "," + p5 + "\n")