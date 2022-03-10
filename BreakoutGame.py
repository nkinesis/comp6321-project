import sys, pygame
import GameObjects

class BreakoutGame():

    def __init__(self):
        self._observers = []

    def attach(self, observer: GameObjects.Observer) -> None:
        self._observers.append(observer)

    def detach(self,observer: GameObjects.Observer) -> None:
        self._observers.remove(observer)

    def notify(self, event: GameObjects.Event) -> None:
        for observer in self._observers:
            observer.update(event)

    def initGame(self):
        self.score = 0  
        self.wall = None
        self.ball_xspeed = GameObjects.BALL_XSPEED
        self.ball_yspeed = GameObjects.BALL_YSPEED
        self.lives = GameObjects.MAX_LIVES
        self.bat_speed = GameObjects.BAT_XSPEED
        self.size = self.width, self.height = 640, 480
        self.gameScreen = None
        self.gameClock = None
        self.gameSound = None

        self.initGraphics()
        self.initSound()
        self.initObjects()
        event = GameObjects.Event(self.score, self.lives, self.bat, self.ball)
        self.notify(event)

    def initGraphics(self):
        pygame.init()  
        self.gameScreen = pygame.display.set_mode(self.size)
        self.gameClock = pygame.time.Clock()
        pygame.mouse.set_visible(0) 

    def initSound(self):
        self.gameSound = pygame.mixer.Sound('assets/blip.wav')
        self.gameSound.set_volume(0) #original: 10   

    def initObjects(self):
        # wall
        self.wall = GameObjects.Wall()
        self.wall.build_wall(self.width)

        # bat and ball
        self.bat = GameObjects.Bat()
        self.ball = GameObjects.Ball()
        self.bat.rect = self.bat.rect.move((self.width / 2) - (self.bat.rect.right / 2), self.height - 20)
        self.ball.rect = self.ball.rect.move(self.width / 2, self.height / 2)

    def runLogic(self, comm):
        self.checkAgentCommands(comm)
        self.checkCollision()  
        self.moveBall()  
        self.checkLosingCondition()  
        self.checkIfBallOutOfBounds()  
        self.checkBallHitWall()    
        self.checkHumanQuit() 
        event = GameObjects.Event(self.score, self.lives, self.bat, self.ball)
        self.notify(event)

    def checkAgentCommands(self, comm):
        if comm == 0:                        
            self.bat.rect = self.bat.rect.move(-self.bat_speed, 0)     
            if (self.bat.rect.left < 0):                           
                self.bat.rect.left = 0      
        if comm == 1:                    
            self.bat.rect = self.bat.rect.move(self.bat_speed, 0)
            if (self.bat.rect.right > self.width):                            
                self.bat.rect.right = self.width
                      
    def checkCollision(self):
        if self.ball.isCollided(self.bat.rect):
            self.ball_yspeed = -self.ball_yspeed                
            self.gameSound.play(0)                
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

    def moveBall(self):
        # move and limit movement in the edges of the screen
        self.ball.rect = self.ball.rect.move(self.ball_xspeed, self.ball_yspeed)

        if self.ball.rect.left < 0 or self.ball.rect.right > self.width:
            self.ball_xspeed = -self.ball_xspeed                
            self.gameSound.play(0)            
        if self.ball.rect.top < 0:
            self.ball_yspeed = -self.ball_yspeed                
            self.gameSound.play(0)        

    def checkLosingCondition(self):
        # if ball is below screen height, lose 1 life
        # put a new ball into the game
        if self.ball.rect.top > self.height:
            self.lives -= 1    
            self.ball_xspeed = GameObjects.BALL_XSPEED
            self.ball_yspeed = GameObjects.BALL_YSPEED            
            self.ball.rect.center = self.width / 2, self.height / 3  

        if self.lives == 0:    
            event = GameObjects.Event(self.score, self.lives, self.bat, self.ball)
            self.notify(event)
            self.initGame() #restart game

    def checkIfBallOutOfBounds(self):
        if self.ball_xspeed < 0 and self.ball.rect.left < 0:
            self.ball_xspeed = -self.ball_xspeed                                
            self.gameSound.play(0)

        if self.ball_xspeed > 0 and self.ball.rect.right > self.width:
            self.ball_xspeed = -self.ball_xspeed                               
            self.gameSound.play(0)

    def checkBallHitWall(self):
        index = self.ball.rect.collidelist(self.wall.brickrect)       
        if index != -1: 
            if self.ball.rect.center[0] > self.wall.brickrect[index].right or \
                self.ball.rect.center[0] < self.wall.brickrect[index].left:
                self.ball_xspeed = -self.ball_xspeed
            else:
                self.ball_yspeed = -self.ball_yspeed                
            self.gameSound.play(0)              
            self.wall.brickrect[index:index + 1] = []
            self.score += 10
        
    def render(self):
        self.gameClock.tick(60)

        self.gameScreen.fill(GameObjects.BG_COLOR)
        scoretext, scoretextrect = GameObjects.drawScore(self.score, self.width)
        self.gameScreen.blit(scoretext, scoretextrect)

        for i in range(0, len(self.wall.brickrect)):
            self.gameScreen.blit(self.wall.brick, self.wall.brickrect[i])    

        # if wall completely gone then rebuild it
        if self.wall.brickrect == []:              
            self.wall.build_wall(self.width)                
            self.ball_xspeed = GameObjects.BALL_XSPEED
            self.ball_yspeed = GameObjects.BALL_YSPEED              
            self.ball.rect.center = self.width / 2, self.height / 3
        
        self.gameScreen.blit(self.ball.sprite, self.ball.rect)
        self.gameScreen.blit(self.bat.sprite, self.bat.rect)
        pygame.display.flip()

    def checkHumanQuit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
    
    def main(self):
        self.initGame()
        while True:
            self.runLogic(0)
            self.render()


        


