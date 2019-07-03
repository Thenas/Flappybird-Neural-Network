import pygame
from os import system as sys
import threading
from random import randint as rand

#Constantes
GRAV = 1
H = 650
W = 450
RUN = True
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
global SCORE; SCORE = 0
# Fin Constantes

def collition(bird ,pipe):
    global SCORE
    rangoB = set(range(bird.x - bird.r, bird.x + bird.r))
    rangoP = set(range(pipe.x, pipe.x+pipe.ancho))  
    res = rangoB.intersection(rangoP)


    
    rangoB  = set(range(int(bird.y) - bird.r, int(bird.y) + bird.r))
    rangoP = set(range(pipe.y, pipe.y + pipe.largo))  
    res2 = rangoB.intersection(rangoP)

    if    (pipe.x + pipe.ancho)  < (bird.x - bird.r) < (pipe.x + pipe.ancho + 2)   : bird.score+=1

    if res and not res2: return True
    else: return False
    
class birds:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.originaly = y
        self.originalvy = 0.1
        self.r = 20
        self.vy = 0.1
        self.t = 0
        self.score = 0
    def update(self):
        self.vy += GRAV
        self.y += self.vy 
        

        if self.y > H : 
            self.vy = 0
            self.y = H
         

    def draw(self, wind):
        pygame.draw.circle(wind, (244, 241, 66), (self.x, int(self.y)), self.r)
        self.update()


    def up(self):
       self.vy = -10

class pipe:
    def __init__(self,x= W):
        

        self.x = x 
        self.ancho = 65
        self.largo = 120
        self.y = int(rand(25,75)*H/100)


        self.color = GREEN
    def draw(self, wind):
        pygame.draw.rect(wind, self.color, (self. x,0 , self.ancho, self.y))
        #pygame.draw.rect(wind, self.color, (self.x, self.y, self.ancho, self.largo)) # area para pasar
        pygame.draw.rect(wind, self.color, (self. x ,self.y + self.largo , self.ancho, H))
        self.x-=2
        if (self.x+ self.ancho) < 0:
             self.x = W-20
             self.y = int(rand(25,75)*H/100)  
         




bird = birds(100,int(640/2))
pipes = [pipe(), pipe(x=W +250)]

pygame.init()
win = pygame.display.set_mode((W,H))
pygame.display.set_caption("fappy bird :V")





while RUN:
    for event in pygame.event.get():
        keyPressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT: RUN = False
        if(keyPressed[pygame.K_SPACE] and event.type == pygame.KEYDOWN): bird.up()
    win.fill((112, 196, 207))
    pygame.time.delay(17)

    
    #if(collition(bird,pipe1)):pipe1.color = (255,0,0)
    #else: pipe1.color = (0,255,0)   

    for Pipe in pipes:
         if collition(bird, Pipe): Pipe.color = RED
         else: Pipe.color = GREEN
         Pipe.draw(win)
    bird.draw(win)
    pygame.display.update()    
    print(bird.score)  
    
     


