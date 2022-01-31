import math
import random
import pygame

pygame.init()
width=720
height=580
screen=pygame.display.set_mode((width,height))

pygame.display.set_caption("Space Invaders by Adam Červenka")
icon1=pygame.image.load("alien.png")
pygame.display.set_icon()

enemies_count=10
enemies=[]
enemiesX=[]
enemiesY=[]
enemiesX_change=[]
enemiesY_change=[]
for i in range enemies_count:
    enemies.append(pygame.image.load("alien.png"))
    enemiesX.append(random.randint(30,width-30))
    enemiesY.append(random.randint(20,height//2,5))
    enemiesX_change.append(2)
    enemiesY_change.append(20)


rocket=pygame.image.load("rocket.png")
rocketX=width//2
rocketY=height-120
rocketX_change=0


