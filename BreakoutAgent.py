from stable_baselines3 import PPO

import gym
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
    info = {}

    ball = self.observer.event.ball.rect
    bat = self.observer.event.bat.rect
    dif_l = abs(ball.left - bat.left)
    dif_r = abs(ball.right - bat.right)    
    if dif_l < 50 or dif_r < 50:
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

    run_last_agent_trained = True
    env = BreakoutAgent()

    if run_last_agent_trained:
      obs = env.reset()
      model = PPO.load("breakout_model")
    else:
      model = PPO('MlpPolicy', env, verbose=1)
      model.learn(total_timesteps=100000)
      obs = env.reset()
      model.save("breakout_model")

    for i in range(4000):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            obs = env.reset()