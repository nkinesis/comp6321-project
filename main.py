from stable_baselines3 import PPO

import gym
import pygame
import numpy as np
import random
import sys
from wall import Wall
from gym import spaces

class BreakoutEnv(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}
  
  # Action Constants
  LEFT = 0
  RIGHT = 1

  def __init__(self):
    super(BreakoutEnv, self).__init__()

    # Game variables
    self.xspeed_init = 1 #2.5
    self.yspeed_init = 1
    self.max_lives = 5
    self.bat_speed = 15
    self.score = 0 
    self.bgcolour = 0x2F, 0x4F, 0x4F  # darkslategrey        
    self.size = self.width, self.height = 640, 480

    # Initialise game window
    pygame.init()
    pygame.display.set_caption('Breakout')
    print("initializing...")
    self.clock = pygame.time.Clock()
    self.screen = pygame.display.set_mode(self.size)

    self.bat = pygame.image.load("assets/bat.png").convert()
    self.batrect = self.bat.get_rect()

    self.ball = pygame.image.load("assets/ball.png").convert()
    self.ball.set_colorkey((255, 255, 255))
    self.ballrect = self.ball.get_rect()
    
    self.soundCtrl = pygame.mixer.Sound('assets/blip.wav')
    self.soundCtrl.set_volume(0)        
    
    self.wall = Wall()
    self.wall.build_wall(self.width)

    # Initialise ready for game loop
    self.batrect = self.batrect.move((self.width / 2) - (self.batrect.right / 2), self.height - 20)
    self.ballrect = self.ballrect.move(self.width / 2, self.height / 2)       

    self.xspeed = self.xspeed_init
    self.yspeed = self.yspeed_init
    self.lives = self.max_lives

    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions:
    number_of_actions = 2
    number_of_observations = 4
    self.action_space = spaces.Discrete(number_of_actions)
    
    # Example for using image as input (channel-first; channel-last also works):
    self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(number_of_observations,), dtype=np.float32)

  def step(self, action):
    # exit if ESC is pressed by a human
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
          sys.exit()

    # let agent move the bat
    if action == self.LEFT:
      self.batrect = self.batrect.move(-self.bat_speed, 0)     
      if (self.batrect.left < 0):                           
          self.batrect.left = 0  
    if action == self.RIGHT:
      self.batrect = self.batrect.move(self.bat_speed, 0)
      if (self.batrect.right > self.width):                            
          self.batrect.right = self.width
    self.show_score()

    # check if bat has hit ball    
    if self.ballrect.bottom >= self.batrect.top and \
        self.ballrect.bottom <= self.batrect.bottom and \
        self.ballrect.right >= self.batrect.left and \
        self.ballrect.left <= self.batrect.right:
        self.yspeed = -self.yspeed                
        self.soundCtrl.play(0)                
        offset = self.ballrect.center[0] - self.batrect.center[0]   
        self.score += 1 # reward +                   
        # offset > 0 means ball has hit RHS of bat                   
        # vary angle of ball depending on where ball hits bat                      
        if offset > 0:
            if offset > 30:  
                self.xspeed = 7
            elif offset > 23:                 
                self.xspeed = 6
            elif offset > 17:
                self.xspeed = 5 
        else:  
            if offset < -30:                             
                self.xspeed = -7
            elif offset < -23:
                self.xspeed = -6
            elif self.xspeed < -17:
                self.xspeed = -5     
              
    # move bat/ball
    self.ballrect = self.ballrect.move(self.xspeed, self.yspeed)
    if self.ballrect.left < 0 or self.ballrect.right > self.width:
        self.xspeed = -self.xspeed                
        self.soundCtrl.play(0)            
    if self.ballrect.top < 0:
        self.yspeed = -self.yspeed                
        self.soundCtrl.play(0)   

    # check if ball has gone past bat, lose a life
    if self.ballrect.top > self.height:
        self.lives -= 1
        self.score -= 100 # reward -
        # start a new ball
        self.xspeed = self.xspeed_init          
        if random.random() > 0.5:
            self.xspeed = -self.xspeed 
        self.yspeed = self.yspeed_init            
        self.ballrect.center = self.width * random.random(), self.height / 3                                
    if self.xspeed < 0 and self.ballrect.left < 0:
        self.xspeed = -self.xspeed                                
        self.soundCtrl.play(0)

    if self.xspeed > 0 and self.ballrect.right > self.width:
        self.xspeed = -self.xspeed                               
        self.soundCtrl.play(0)
    
    # check if ball has hit wall
    # if yes yhen delete brick and change ball direction
    index = self.ballrect.collidelist(self.wall.brickrect)       
    if index != -1: 
        if self.ballrect.center[0] > self.wall.brickrect[index].right or \
            self.ballrect.center[0] < self.wall.brickrect[index].left:
            self.xspeed = -self.xspeed
        else:
            self.yspeed = -self.yspeed                
        self.soundCtrl.play(0)              
        self.wall.brickrect[index:index + 1] = []
        self.score += 100 # reward +

    # if wall completely gone then rebuild it
    if self.wall.brickrect == []:              
        self.wall.build_wall(self.width)                
        self.xspeed = self.xspeed_init
        self.yspeed = self.yspeed_init                
        self.ballrect.center = self.width / 2, self.height / 3

    # reward for following the ball
    dif_l = abs(self.ballrect.left - self.batrect.left)
    dif_r = abs(self.ballrect.right - self.batrect.right)    
    if dif_l < 50 or dif_r < 50:
        self.score += 10
    else:
        self.score -= 10

    reward = self.score
    done = (self.lives == 0)
    info = {}

    return np.array([self.batrect.left, self.batrect.right, self.ballrect.left, self.ballrect.right], dtype=np.float32), reward, done, info

  def reset(self):
      self.screen.fill(self.bgcolour)
      self.wall.build_wall(self.width)
      self.lives = self.max_lives
      self.score = 0
      return np.array([self.batrect.left, self.batrect.right, self.ballrect.left, self.ballrect.right], dtype=np.float32)

  def render(self, mode='human'):
      self.screen.fill(self.bgcolour)
      scoretext = pygame.font.Font(None,40).render(str(self.score), True, (0,255,255), self.bgcolour)
      scoretextrect = scoretext.get_rect()
      scoretextrect = scoretextrect.move(self.width - scoretextrect.right, 0)
      self.screen.blit(scoretext, scoretextrect)

      for i in range(0, len(self.wall.brickrect)):
          self.screen.blit(self.wall.brick, self.wall.brickrect[i])    
    
      self.screen.blit(self.ball, self.ballrect)
      self.screen.blit(self.bat, self.batrect)
      pygame.display.flip()
      self.clock.tick(60)

  def close(self):
      pygame.quit()
      sys.exit()

  def show_score(self):
      print(self.score)
      print("=====")

if __name__=="__main__":
    env = BreakoutEnv()
    model = PPO('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=100000) #100000
    obs = env.reset()

    for i in range(2000):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            obs = env.reset()
