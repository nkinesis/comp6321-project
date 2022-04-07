import pygame

BALL_XSPEED=2.5
BALL_YSPEED=2.5
BAT_XSPEED=15
MAX_LIVES=5
BG_COLOR = 0x2F, 0x4F, 0x4F 

def load_game_obj(name):
    return pygame.image.load("game/assets/%s.png" % name).convert().get_rect()

def draw_score_value(text, width):
    scoretext = pygame.font.Font(None,40).render(str(text), True, (0,255,255), BG_COLOR)
    scoretextrect = scoretext.get_rect()
    scoretextrect = scoretextrect.move(width - scoretextrect.right, 0)
    return scoretext, scoretextrect

class Ball():
    def __init__(self):
        self.sprite = pygame.image.load("game/assets/ball.png").convert()
        self.rect = self.sprite.get_rect()

    def move(self, x, y):
        self.rect.move(x, y)

    def is_collided(self, rect):
        return self.rect.bottom >= rect.top and self.rect.bottom <= rect.bottom and self.rect.right >= rect.left and self.rect.left <= rect.right

class Bat():
    def __init__(self):
        self.sprite = pygame.image.load("game/assets/bat.png").convert()
        self.rect = self.sprite.get_rect()

    def move(self, x, y):
        self.rect.move(x, y)

class Wall():
    
    def __init__(self):
        self.brick = pygame.image.load("game/assets/brick.png").convert()
        brickrect = self.brick.get_rect()
        self.bricklength = brickrect.right - brickrect.left       
        self.brickheight = brickrect.bottom - brickrect.top             

    def build_wall(self, width):        
        xpos = 0
        ypos = 60
        adj = 0
        self.brickrect = []
        for i in range (0, 52):           
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

class Event():
    def __init__(self, score, lives, bat, ball):
        self.score = score
        self.lives = lives
        self.bat = bat
        self.ball = ball

class Observer():
    def __init__(self):
        self.event = None

    def update(self, event: Event):
        self.event = event