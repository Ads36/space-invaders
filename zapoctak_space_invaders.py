import math
import random
import pygame

pygame.init()
width=720
height=580
screen=pygame.display.set_mode((width,height))
black=pygame.Color(0,0,0)
white=pygame.Color(255,255,255)
clock=pygame.time.Clock()

pygame.display.set_caption("Space Invaders by Adam Červenka")
icon1=pygame.image.load("alien1.png")
pygame.display.set_icon(icon1)

score=0
direction=0
enemies_count=15
enemies=[]
enemiesX=[]
enemiesY=[]
enemiesX_change=[]
enemiesY_change=50
for i in range(enemies_count):
    enemies.append(pygame.image.load("alien1.png"))
    enemiesX.append(random.randint(0,width-64))
    enemiesY.append(random.randint(20,height//3))
    enemiesX_change.append(random.choice((-2,2)))
    
rocket=pygame.image.load("rocket1.png")
rocketX=width//2
rocketY=height-100
rocketX_change=7

bullet=pygame.image.load("bullet1.png")
bulletX=rocketX
bulletY=rocketY
bulletY_change=15
bullet_fired=False

text=pygame.font.Font("bebas.ttf",30)
def draw_score(score):
    score1=text.render("Score: "+str(score),True,white)
    screen.blit(score1,(15,10))
def draw_rocket(x,y):
    screen.blit(rocket,(x,y))
def draw_enemy(which,x,y):
    screen.blit(enemies[which],(x,y))
def draw_bullet(x,y):
    screen.blit(bullet,(x+15,y+10))
def enemy_bullet_collision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance<35:
        return True
    else:
        return False
def rocket_bomb_collision(rocketX,rocketY,bombX,bombY):
    distance=math.sqrt(math.pow(rocketX-bombX,2)+math.pow(rocketY-bombY,2))
    if distance<35:
        return True
    else:
        return False

is_running=True
while is_running:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            is_running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                direction=-1
            if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                direction=1
            if event.key==pygame.K_SPACE:
                #vystřel
                if bullet_fired is False:
                    bullet_fired=True
                    bulletX=rocketX
                    
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_a or event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                direction=0
                
    if direction==-1:
        rocketX-=rocketX_change
    if direction==1:
        rocketX+=rocketX_change
    
    if rocketX>=width-40:
        rocketX=width-40
    if rocketX<=0:
        rocketX=0
    for which in range(enemies_count):

        enemiesX[which]+=enemiesX_change[which]
        if enemiesX[which]<0:
            enemiesX_change[which]=-enemiesX_change[which]
            enemiesY[which]+=enemiesY_change

        if enemiesX[which]>width-64:
            enemiesX_change[which]=-enemiesX_change[which]
            enemiesY[which]+=enemiesY_change

        if bullet_fired:
            if enemy_bullet_collision(enemiesX[which],enemiesY[which],bulletX,bulletY):
                bullet_fired=False
                bulletY=rocketY
                score+=1
                enemiesX[which]=random.randint(30,width-64)
                enemiesY[which]=random.randint(20,height//2.5)

        draw_enemy(which,enemiesX[which],enemiesY[which])

    if bullet_fired:
        draw_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    if bulletY<=0:
        bullet_fired=False
        bulletY=rocketY
    draw_rocket(rocketX,rocketY)
    draw_score(score)
    clock.tick(60)
    pygame.display.flip()
