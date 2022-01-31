import math
import random
import pygame

pygame.init()
width=720
height=580
screen=pygame.display.set_mode((width,height))
black=pygame.Color(0,0,0)

pygame.display.set_caption("Space Invaders by Adam Červenka")
icon1=pygame.image.load("alien1.png")
pygame.display.set_icon(icon1)

enemies_count=10
enemies=[]
enemiesX=[]
enemiesY=[]
enemiesX_change=[]
enemiesY_change=[]
for i in range(enemies_count):
    enemies.append(pygame.image.load("alien1.png"))
    enemiesX.append(random.randint(30,width-30))
    enemiesY.append(random.randint(20,height//2.5))
    enemiesX_change.append(2)
    enemiesY_change.append(20)


rocket=pygame.image.load("rocket1.png")
rocketX=width//2
rocketY=height-120
rocketX_change=0

bullet_fired=False

def draw_rocket(x,y):
    screen.blit(rocket,(x,y))



is_running=True
while is_running:
    screen.fill(black)
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            is_running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                rocketX_change=-10
            if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                rocketX_change=10
            if event.key==pygame.K_SPACE:
                #vystřel
                if not bullet_fired:
                    pass
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_a or event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                rocketX_change=0

    rocketX+=rocketX_change
    if rocketX>=width:
        rocketX=width
    if rocketX<=0:
        rocketX=0

    draw_rocket(rocketX,rocketY)
    pygame.display.update()
