import numpy
import pygame
from breakout_agent import BreakoutAgent
import game.breakout_objects as BreakoutObjects

# check initial agent state
env = BreakoutAgent()
assert type(env.observer) is BreakoutObjects.Observer, "observer was not initialized correctly"
assert env.prevScore == 0, "initial prev score should equal zero"

# reset
obs = env.reset()
assert type(obs) is numpy.ndarray, "unexpected type, reset should return numpy.ndarray"
assert len(obs) == 4, "unexpected length, expected 4 observations"
assert obs[2] == 280, "unexpected bat initial x position"
assert obs[3] == 360, "unexpected bat initial y position"

# do step, move left
obs = env.step(0)
assert type(obs) is tuple, "unexpected type, step should return tuple"
assert len(obs[0]) == 4, "unexpected length, expected 4 observations"
assert obs[0][2] <= 280, "unexpected bat x position, should have moved left"

# do step, move right
obs = env.step(1)
assert type(obs) is tuple, "unexpected type, step should return tuple"
assert len(obs[0]) == 4, "unexpected length, expected 4 observations"
assert obs[0][2] >= 280, "unexpected bat x position, should have moved right"

# render game on screen
screen = env.render()
assert type(screen) is pygame.Surface, "the game screen was not rendered correctly"