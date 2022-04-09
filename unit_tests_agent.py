import numpy
import pygame
from breakout_agent import BreakoutAgent
import game.breakout_objects as BreakoutObjects

""" All functions were written by Gabriel C. Ullmann, unless otherwise noted.
Unit testing the OpenAI Gym environment (agent).

Check initial agent state. """
env = BreakoutAgent()
assert isinstance(
    env.observer, BreakoutObjects.Observer), "observer was not initialized correctly"
assert env.prevScore == 0, "initial prev score should equal zero"

""" Check reset state. """
obs = env.reset()
assert isinstance(
    obs, numpy.ndarray), "unexpected type, reset should return numpy.ndarray"
assert len(obs) == 4, "unexpected length, expected 4 observations"
assert obs[2] == 280, "unexpected bat initial x position"
assert obs[3] == 360, "unexpected bat initial y position"

""" Check step, move left. """
obs = env.step(0)
assert isinstance(obs, tuple), "unexpected type, step should return tuple"
assert len(obs[0]) == 4, "unexpected length, expected 4 observations"
assert obs[0][2] <= 280, "unexpected bat x position, should have moved left"

""" Check step, move right. """
obs = env.step(1)
assert isinstance(obs, tuple), "unexpected type, step should return tuple"
assert len(obs[0]) == 4, "unexpected length, expected 4 observations"
assert obs[0][2] >= 280, "unexpected bat x position, should have moved right"

""" Check render game on screen. """
screen = env.render()
assert isinstance(
    screen, pygame.Surface), "the game screen was not rendered correctly"

print("Correct!")
