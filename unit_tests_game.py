import pygame
from game.breakout_game import BreakoutGame
import game.breakout_objects as breakout_objects

""" All functions were written by Gabriel C. Ullmann, unless otherwise noted.
Unit testing the Breakout game and related helper functions.

Initialize instance of pygame, not running Breakout yet """
pygame.init()  
size = width, height = 640, 480
pygame.display.set_mode(size)

""" Check sprite loading """
ball = breakout_objects.load_game_obj('ball')
assert type(ball) is pygame.Rect, "unexpected type returned, expected pygame.Rect"
assert ball.width == 17, "unexpected sprite width"
assert ball.height == 17, "unexpected sprite height"

""" Check text drawing """
text, rect = breakout_objects.draw_text('lorem ipsum', 10)
assert type(text) is pygame.Surface, "the text was not rendered correctly"
assert type(rect) is pygame.Rect, "unexpected type returned, expected pygame.Rect"
assert rect.top == 0, "unexpected text y position, should be on the top of the screen"

""" Check wall building """
wall = breakout_objects.Wall()
assert type(wall.brick) is pygame.Surface, "brick sprite was not rendered correctly"
wall.build_wall(width)
assert type(wall.brickrect) is list, "wall was not built correctly"
assert len(wall.brickrect) > 0, "wall was not built correctly"

""" Initialize and run one step of Breakout, record ball/bat positions """
game = BreakoutGame()
game.init_game()
game.run_logic(0)
assert type(game.gameScreen) is pygame.Surface, "the game was not rendered correctly"
assert type(game.ball) is breakout_objects.Ball, "ball object was not initialized correctly"
assert type(game.bat) is breakout_objects.Bat, "bat object was not initialized correctly"
ball_xpos = game.ball.rect.left
bat_xpos = game.bat.rect.left

""" Run another step of Breakout, check for position updates """
game.run_logic(0)
assert game.ball.rect.left != ball_xpos, "ball position is not being updated correctly"
assert game.bat.rect.left != bat_xpos, "bat position is not being updated correctly"

print("Correct!")