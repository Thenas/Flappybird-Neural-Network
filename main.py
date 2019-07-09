import pygame
from os import system as sys
import threading
from random import randint as rand
from time import sleep
import NeuralNet as nNet
import numpy as np

#------------------Constantes--------------#
GRAV = 1
H = 650
W = 500
RUN = True
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
TOTAL = 50
ARQUI = [2,3,1]
global GEN;GEN = 0

#--------------------------------------------#




#-------------funciones----------------------#
def crossOver(bird1,bird2):
    if rand(0,100)>50:

        birdChild = birds(y = bird1.y)
        birdChild.nn.weights[0] = bird1.nn.weights[0]
        birdChild.nn.weights[1] = bird2.nn.weights[1]

    else: 
        birdChild = birds(y = bird2.y)
        birdChild.nn.weights[0] = bird2.nn.weights[0]
        birdChild.nn.weights[1] = bird1.nn.weights[1]


    return birdChild

def shift(l, n): return l[n:] + l[:n]

def collition(bird ,pipe):
    Xcollition  = (pipe.x <(bird.x+bird.r)< pipe.x + pipe.ancho) or (pipe.x<(bird.x - bird.r)< pipe.x + pipe.ancho) 
    Ycollition  =  ((bird.y + bird.r) > (pipe.y + pipe.largo))  or  ((bird.y - bird.r) < pipe.y)
    return Xcollition and Ycollition
#--------------------------------------------#


#---------------Clases-----------------------#



class birds:
    def __init__(self,y):
        self.x = 100
        self.y = y
        self.r = 20
        self.vy = 0.1
        self.score = 0
        self.nn = nNet.NeuralNetwork(ARQUI,activation="tanh")
        self.image = pygame.image.load('sprite1.png')
        
    def update(self):
        self.vy += GRAV
        self.y += self.vy 
        self.score+=1

        if self.y > H : 
            self.vy = 0
            self.y = H
         

    def draw(self, wind):
       # pygame.draw.circle(wind, (244, 241, 66), (self.x, int(self.y)), self.r)
        wind.blit(self.image, (self.x - self.r  , self.y - self.r))
        self.update()


    def think(self, pipe):
       X = np.array([self.y,(pipe.y + (pipe.largo/2))])
       if self.nn.predict(X)>0: self.vy = -10
        
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
  
    def update(self):
        if self.x + self.ancho < 0:
            self.x = W +20
            self.y = int(rand(25,75)*H/100)
            return True
#--------------------------------------------#   

#--------inicialización de pygame------------#
 
pygame.init()
win = pygame.display.set_mode((W,H))
pygame.display.set_caption("fappy bird :V")
#--------------------------------------------#


#----------------setup-----------------------#
pajaros = []
pipes = []
lovePool = []
deadPool = []

for i in range(TOTAL):pajaros.append(birds(y=int(rand(10,90)*H/100)))
for i in range(2):pipes.append(pipe(x=W + 300*i))



#--------------------------------------------#
while RUN:
    for event in pygame.event.get():
        keyPressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT: RUN = False
    win.fill((112, 196, 207))


#-----------------Draw-----------------------#
   
    for pip in pipes:
        if pipes[0].update():
             pipes.remove(pipes[0])
             pipes.append(pipe())
        pip.draw(win)
        
        pygame.draw.circle(win, (0,0,0), (pipes[0].x + int(pipes[0].ancho/2),40), 15)

    for pajaro in pajaros:
        pajaro.think(pipes[0])

        if collition(pajaro, pipes[0]):
            deadPool.append(pajaro)
            pajaros.remove(pajaro)
        pajaro.draw(win)
    
#--------------------------------------------#

#-----------------Coques y demas ------------#


#--------------------------------------------#




    pygame.time.delay(10)
    pygame.display.update()  
  

    
 



