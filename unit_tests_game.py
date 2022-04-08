import pygame
import game.breakout_objects as breakout_objects

# initialize instance of pygame 
pygame.init()  
size = width, height = 640, 480
pygame.display.set_mode(size)

# sprite loading
ball = breakout_objects.load_game_obj('ball')
assert type(ball) is pygame.Rect, "unexpected type returned, expected pygame.Rect"
assert ball.width == 17, "unexpected sprite width"
assert ball.height == 17, "unexpected sprite height"

# text drawing
text, rect = breakout_objects.draw_text('lorem ipsum', 10)
assert type(text) is pygame.Surface, "the text was not rendered correctly"
assert type(rect) is pygame.Rect, "unexpected type returned, expected pygame.Rect"
assert rect.top == 0, "unexpected text y position, should be on the top of the screen"

# wall building
wall = breakout_objects.Wall()
assert type(wall.brick) is pygame.Surface, "brick sprite was not rendered correctly"
wall.build_wall(width)
assert type(wall.brickrect) is list, "wall was not built correctly"
assert len(wall.brickrect) > 0, "wall was not built correctly"

