import pygame

""" All functions were written by Gabriel C. Ullmann, unless otherwise noted.
Main game variables: initial ball and bat speed, number of lives, background color"""
BALL_XSPEED = 2.5
BALL_YSPEED = 2.5
BAT_XSPEED = 15
MAX_LIVES = 5
BG_COLOR = 0x2F, 0x4F, 0x4F

"""Load a sprite and create a pygame.Rect object from it.

Arguments
---------
name : string
    Name of the sprite inside the assets folder.

Returns
---------
    A pygame.Rect.
"""


def load_game_obj(name):
    return pygame.image.load("game/assets/%s.png" % name).convert().get_rect()


"""Create a pygame.Font object with text and draw it on the top of the screen.

Arguments
---------
text : string
    The text to be drawn. Maximum 20 characters.

width : int
    Position X of the text on the screen. Position Y is always 0 (top of the screen).

Returns
---------
    A pygame.Surface (text already rendered on-screen) and a pygame.Rect.
"""


def draw_text(text, x_pos):
    text = str(text)
    text = (text[:20] + '...') if len(text) > 20 else text
    scoretext = pygame.font.Font(None, 40).render(
        str(text), True, (0, 255, 255), BG_COLOR)
    scoretextrect = scoretext.get_rect()
    scoretextrect = scoretextrect.move(x_pos - scoretextrect.right, 0)
    return scoretext, scoretextrect


"""Class representing the ball object of the game.

Author: John Cheetham, 2009.
"""


class Ball():
    def __init__(self):
        self.sprite = pygame.image.load("game/assets/ball.png").convert()
        self.rect = self.sprite.get_rect()

    """Move the ball to a point on the screen.

    Arguments
    ---------
    x : int
        Coordinate x on screen

    y : int
        Coordinate y on screen
    """

    def move(self, x, y):
        self.rect.move(x, y)

    """Check whether the ball has collided with a given pygame.Rect object.

    Arguments
    ---------
    rect : pygame.Rect
        The pygame.Rect object you want to check for collision.

    Returns
    ---------
        A boolean value: True if colliding, False otherwise.
    """

    def is_collided(self, rect):
        return self.rect.bottom >= rect.top and self.rect.bottom <= rect.bottom and self.rect.right >= rect.left and self.rect.left <= rect.right


"""Class representing the bat object of the game.

Author: John Cheetham, 2009
"""


class Bat():
    def __init__(self):
        self.sprite = pygame.image.load("game/assets/bat.png").convert()
        self.rect = self.sprite.get_rect()

    """Move the ball to a point on the screen.

    Arguments
    ---------
    x : int
        Coordinate x on screen.

    y : int
        Coordinate y on screen.
    """

    def move(self, x, y):
        self.rect.move(x, y)


"""Class representing the wall object (brick) of the game.

Author: John Cheetham, 2009.
"""


class Wall():
    def __init__(self):
        self.brick = pygame.image.load("game/assets/brick.png").convert()
        brickrect = self.brick.get_rect()
        self.bricklength = brickrect.right - brickrect.left
        self.brickheight = brickrect.bottom - brickrect.top

    """Build a wall composed of several bricks on the top of the screen

    Arguments
    ---------
    width : int
        Width covered by the wall, in pixels
    """

    def build_wall(self, width=100):
        xpos = 0
        ypos = 60
        adj = 0
        self.brickrect = []
        for i in range(0, 52):
            if xpos > width:
                if adj == 0:
                    adj = self.bricklength / 2
                else:
                    adj = 0
                xpos = -adj
                ypos += self.brickheight

            self.brickrect.append(self.brick.get_rect())
            self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
            xpos = xpos + self.bricklength


"""Class representing a game state change event."""


class Event():
    def __init__(self, score, lives, bat, ball):
        self.score = score
        self.lives = lives
        self.bat = bat
        self.ball = ball


"""Observer class that watches/notifies game state changes."""


class Observer():
    def __init__(self):
        self.event = None

    """When a game state is notified, update this is information for all attached observers.

    Arguments
    ---------
    event : Event
        A game state change event.
    """

    def update(self, event: Event):
        self.event = event
