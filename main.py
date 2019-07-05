import pygame
from os import system as sys
import threading
from random import randint as rand
from time import sleep
import NeuralNet as nNet
import numpy as np

#Constantes
GRAV = 1
H = 650
W = 450
RUN = True
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
TOTAL = 50
global GEN;GEN = 0

# Fin Constantes

def nextGen(pajaros, pipes) :
    global GEN
    scores = [] #guarda tuplas con el indice del pajaro y su puntuacion 
    for i in range(len(pajaros)):
        scores.append((i,pajaros[i].score))
    scores.sort(reverse = True,key= lambda item:item[1])
    parents = [pajaros[scores[0][0]],pajaros[scores[1][0]]]

    w1 = np.array(parents[0].nn.weights)
    w2 = np.array(parents[1].nn.weights)

    wt = (w1+w2)/2
    pajarosNuevos = []

    for i in range(TOTAL):
        pajarosNuevos.append(birds(100,rand(25,75)*H/100))
        pajarosNuevos[i].weights = np.ndarray.tolist(wt * rand(0,100)/100)
    
    pipes[0].x = W
    pipes[1].x = W + 250 
    pipes[0].y = int(rand(25,75)*H/100)
    pipes[1].y = int(rand(25,75)*H/100)

    GEN = GEN + 1
    print("Generacion:",GEN,"          ","PuntacionMax: ", scores[0][1])
    return pajarosNuevos
    



def collition(bird ,pipe):
    Xcollition  = (pipe.x <(bird.x+bird.r)< pipe.x + pipe.ancho) or (pipe.x<(bird.x - bird.r)< pipe.x + pipe.ancho) 
    Ycollition  =  ((bird.y + bird.r) > (pipe.y + pipe.largo))  or  ((bird.y - bird.r) < pipe.y)
    return Xcollition and Ycollition

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
        self.fitness = 0
        self.nn = nNet.NeuralNetwork([6,4,3,2,1],activation="tanh")
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
       X = np.array([self.x,self.y,pipe[0].x,pipe[0].y,pipe[1].x,pipe[1].y])
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
        if (self.x+ self.ancho) < 0:
             self.x = W-20
             self.y = int(rand(25,75)*H/100)  
         
pajarosMuertos = list() 
pajaros = list()
for i in range(TOTAL):pajaros.append(birds(100,rand(25,75)*H/100))
pipes = [pipe(), pipe(x=W +250)]



pygame.init()
win = pygame.display.set_mode((W,H))
pygame.display.set_caption("fappy bird :V")


while RUN:
    for event in pygame.event.get():
        keyPressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT: RUN = False

    win.fill((112, 196, 207))
    #pygame.time.delay(1)


    for Pipe in pipes:
        for pajaro in pajaros:
        
            if collition(pajaro, Pipe): 
                pajarosMuertos.append(pajaro)
                pajaros.pop(pajaros.index(pajaro))
            else: Pipe.color = GREEN
            pajaro.think(pipes)
            pajaro.draw(win)
        Pipe.draw(win) 
    if len(pajaros) == 0: 
        pajaros=nextGen(pajarosMuertos,pipes)
        pajarosMuertos = []
       
    pygame.display.update()  
  

    
 



