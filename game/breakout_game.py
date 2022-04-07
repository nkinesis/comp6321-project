import random
import sys, pygame
import game.breakout_objects as breakout_objects

class BreakoutGame():

    def __init__(self):
        self._observers = []

    def attach(self, observer: breakout_objects.Observer) -> None:
        self._observers.append(observer)

    def detach(self,observer: breakout_objects.Observer) -> None:
        self._observers.remove(observer)

    def notify(self, event: breakout_objects.Event) -> None:
        for observer in self._observers:
            observer.update(event)

    def init_game(self):
        self.score = 0  
        self.wall = None
        self.ball_xspeed = breakout_objects.BALL_XSPEED
        self.ball_yspeed = breakout_objects.BALL_YSPEED
        self.lives = breakout_objects.MAX_LIVES
        self.bat_speed = breakout_objects.BAT_XSPEED
        self.size = self.width, self.height = 640, 480
        self.gameScreen = None
        self.gameClock = None

        self.init_graphics()
        self.init_objects()
        event = breakout_objects.Event(self.score, self.lives, self.bat, self.ball)
        self.notify(event)

    def init_graphics(self):
        pygame.init()  
        self.gameScreen = pygame.display.set_mode(self.size)
        self.gameClock = pygame.time.Clock()
        pygame.mouse.set_visible(0) 

    def init_objects(self):
        # wall
        self.wall = breakout_objects.Wall()
        self.wall.build_wall(self.width)

        # bat and ball
        self.bat = breakout_objects.Bat()
        self.ball = breakout_objects.Ball()
        self.bat.rect = self.bat.rect.move((self.width / 2) - (self.bat.rect.right / 2), self.height - 20)
        self.ball.rect = self.ball.rect.move((self.width / 2) + random.randint(-200, 200), self.height / 2)

    def run_logic(self, comm):
        self.check_agent_commands(comm)
        self.check_collision()  
        self.move_ball()  
        self.check_game_over_condition()  
        self.check_ball_collision_bounds()  
        self.check_ball_hit_wall()    
        self.check_quit_command() 
        event = breakout_objects.Event(self.score, self.lives, self.bat, self.ball)
        self.notify(event)

    def check_agent_commands(self, comm):
        if comm == 0:                        
            self.bat.rect = self.bat.rect.move(-self.bat_speed, 0)     
            if (self.bat.rect.left < 0):                           
                self.bat.rect.left = 0      
        if comm == 1:                    
            self.bat.rect = self.bat.rect.move(self.bat_speed, 0)
            if (self.bat.rect.right > self.width):                            
                self.bat.rect.right = self.width
                      
    def check_collision(self):
        if self.ball.is_collided(self.bat.rect):
            self.ball_yspeed = -self.ball_yspeed                            
            offset = self.ball.rect.center[0] - self.bat.rect.center[0]                          
            # offset > 0 means ball has hit RHS of bat                   
            # vary angle of ball depending on where ball hits bat                      
            if offset > 0:
                if offset > 30:  
                    self.ball_xspeed = 7
                elif offset > 23:                 
                    self.ball_xspeed = 6
                elif offset > 17:
                    self.ball_xspeed = 5 
            else:  
                if offset < -30:                             
                    self.ball_xspeed = -7
                elif offset < -23:
                    self.ball_xspeed = -6
                elif self.ball_xspeed < -17:
                    self.ball_xspeed = -5    

    def move_ball(self):
        # move and limit movement in the edges of the screen
        self.ball.rect = self.ball.rect.move(self.ball_xspeed, self.ball_yspeed)

        if self.ball.rect.left < 0 or self.ball.rect.right > self.width:
            self.ball_xspeed = -self.ball_xspeed                         
        if self.ball.rect.top < 0:
            self.ball_yspeed = -self.ball_yspeed                   

    def check_game_over_condition(self):
        # if ball is below screen height, lose 1 life
        # put a new ball into the game
        if self.ball.rect.top > self.height:
            self.lives -= 1    
            self.ball_xspeed = breakout_objects.BALL_XSPEED
            self.ball_yspeed = breakout_objects.BALL_YSPEED            
            self.ball.rect.center = self.width / 2 + random.randint(-200, 200), self.height / 3  

        if self.lives == 0:    
            event = breakout_objects.Event(self.score, self.lives, self.bat, self.ball)
            self.notify(event)
            #self.initGame() #restart game

    def check_ball_collision_bounds(self):
        if self.ball_xspeed < 0 and self.ball.rect.left < 0:
            self.ball_xspeed = -self.ball_xspeed                                

        if self.ball_xspeed > 0 and self.ball.rect.right > self.width:
            self.ball_xspeed = -self.ball_xspeed                               

    def check_ball_hit_wall(self):
        index = self.ball.rect.collidelist(self.wall.brickrect)       
        if index != -1: 
            if self.ball.rect.center[0] > self.wall.brickrect[index].right or \
                self.ball.rect.center[0] < self.wall.brickrect[index].left:
                self.ball_xspeed = -self.ball_xspeed
            else:
                self.ball_yspeed = -self.ball_yspeed                         
            self.wall.brickrect[index:index + 1] = []
            self.score += 10
        
    def render(self):
        self.gameClock.tick(60)

        self.gameScreen.fill(breakout_objects.BG_COLOR)
        scoretext, scoretextrect = breakout_objects.draw_score_value(self.score, self.width)
        self.gameScreen.blit(scoretext, scoretextrect)

        for i in range(0, len(self.wall.brickrect)):
            self.gameScreen.blit(self.wall.brick, self.wall.brickrect[i])    

        # if wall completely gone then rebuild it
        if self.wall.brickrect == []:              
            self.wall.build_wall(self.width)                
            self.ball_xspeed = breakout_objects.BALL_XSPEED
            self.ball_yspeed = breakout_objects.BALL_YSPEED              
            self.ball.rect.center = self.width / 2, self.height / 3
        
        self.gameScreen.blit(self.ball.sprite, self.ball.rect)
        self.gameScreen.blit(self.bat.sprite, self.bat.rect)
        pygame.display.flip()

    def check_quit_command(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
    
    def main(self):
        self.init_game()
        while True:
            self.run_logic(0)
            self.render()


        



