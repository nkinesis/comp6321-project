from stable_baselines3 import PPO

import gym
import numpy as np
from gym import spaces
from game.breakout_game import BreakoutGame
import game.breakout_objects as BreakoutObjects

""" All functions were written by Gabriel C. Ullmann, unless otherwise noted.
OpenAI Gym environment for playing the Breakout game"""
class BreakoutAgent(gym.Env):

  """ Initialize the agent. It can do 2 actions (go left and right).
  On every step, it will learn based on 4 observations (positions of the ball and the bat)."""
  def __init__(self):
    super(BreakoutAgent, self).__init__()
    number_of_actions = 2
    number_of_observations = 4
    self.action_space = spaces.Discrete(number_of_actions)
    self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(number_of_observations,), dtype=np.float32)
    self.game = BreakoutGame()
    self.observer = BreakoutObjects.Observer()
    self.prevScore = 0
    self.game.attach(self.observer)

  """ On every step, execute game logic, check game state and reward the agent's actions.
  
  Arguments
  ---------
  action : int
      Input generated by the agent, either 0 or 1 (move left or right).
  """
  def step(self, action):
    self.game.run_logic(action)

    reward = 0
    done = (self.observer.event.lives == 0)
    info = {"score": self.observer.event.score, "lives": self.observer.event.lives}

    # if the bat is near the ball, give positive reward
    # otherwise, give negative reward 
    ball = self.observer.event.ball.rect
    bat = self.observer.event.bat.rect
    dif_l = abs(ball.left - bat.left)
    dif_r = abs(ball.right - bat.right)    
    if dif_l < 50 or dif_r < 50:
      reward = 1
    else:
      reward = -1

    # if the score increases, give positive reward
    if self.observer.event.score - self.prevScore > 0:
      reward = 100

    self.prevScore = self.observer.event.score
    return np.array([ball.left, ball.right, bat.left, bat.right], dtype=np.float32), reward, done, info

  """ Make the game go back to its initial state. """
  def reset(self):
    self.game.init_game()
    ball = self.observer.event.ball.rect
    bat = self.observer.event.bat.rect
    return np.array([ball.left, ball.right, bat.left, bat.right], dtype=np.float32)

  """ Draw game on the screen. """
  def render(self):
    self.game.render()
