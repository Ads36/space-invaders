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
def new_enemies(enemies_count):
    global enemies,enemiesX,enemiesY,enemiesX_change,enemiesY_change
    enemies=[]
    enemiesX=[]
    enemiesY=[]
    enemiesX_change=[]
    enemiesY_change=60
    for _ in range(enemies_count):
        enemies.append(pygame.image.load("alien1.png"))
        enemiesX.append(random.randint(0,width-64))
        enemiesY.append(random.randint(20,height//3))
        enemiesX_change.append(random.choice((-5,5)))
    
    
rocket=pygame.image.load("rocket1.png")
rocketX=width//2
rocketY=height-90
rocketX_change=7

bullet=pygame.image.load("bullet1.png")
bulletX=rocketX
bulletY=rocketY
bulletY_change=15
bullet_fired=False

bomb=pygame.image.load("bomb1.png")
bombX=0
bombY=0
bombY_change=5
bombs=[] 
bomb_chance=20

text1=pygame.font.Font("bebas.ttf",30)
text2=pygame.font.Font("bebas.ttf",70)

def draw_score(score):
    score1=text1.render("Score: "+str(score),True,white)
    screen.blit(score1,(15,10))
def draw_rocket(x,y):
    screen.blit(rocket,(x,y))
def draw_enemy(which,x,y):
    screen.blit(enemies[which],(x,y))
def draw_bullet(x,y):
    screen.blit(bullet,(x+18,y))
def draw_bomb(x,y):
    screen.blit(bomb,x,y)
def enemy_bullet_collision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(enemyX+15-bulletX-2,2)+math.pow(enemyY+20-bulletY-5,2))
    if distance<32:
        return True
    else:
        return False
    
def rocket_bomb_collision(rocketX,rocketY,bombX,bombY):
    distance=math.sqrt(math.pow(rocketX-bombX,2)+math.pow(rocketY-bombY,2))
    if distance<35:
        return True
    else:
        return False
def game_over():
    global rocketY,is_game_over
    end=text2.render("Game Over",True,white)
    restart=text1.render("Press space to restart the game",True,white)
    screen.blit(end,(width//3,height//2.5))
    screen.blit(restart,(width//4,height//1.8))
    rocketY=-80
    is_game_over=True

def enemies_actions():
    global score, bullet_fired, bulletX, bulletY
    for which in range(enemies_count):
        if enemiesY[which]+40>=rocketY:
            for i in range(enemies_count):
                enemiesY[i]=height+80
            game_over()
            break

        enemiesX[which]+=enemiesX_change[which]
        if enemiesX[which]<0:
            enemiesX_change[which]=-enemiesX_change[which]
            enemiesY[which]+=enemiesY_change

        if enemiesX[which]>width-64:
            enemiesX_change[which]=-enemiesX_change[which]
            enemiesY[which]+=enemiesY_change

        if bullet_fired is True:
            if enemy_bullet_collision(enemiesX[which],enemiesY[which],bulletX,bulletY):
                bullet_fired=False
                bulletY=rocketY
                score+=1
                enemiesX[which]=random.randint(30,width-64)
                enemiesY[which]=random.randint(20,height//2.5)

        draw_enemy(which,enemiesX[which],enemiesY[which])
        
new_enemies(enemies_count)
is_running=True
is_game_over=False
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
                if is_game_over:
                    score=0
                    new_enemies(enemies_count)
                    is_game_over=False
                    rocketY=height-90
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

    enemies_actions()

    if bullet_fired is True:
        draw_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    if bulletY<=0:
        bullet_fired=False
        bulletY=rocketY
    



    draw_rocket(rocketX,rocketY)
    draw_score(score)
    clock.tick(60)
    pygame.display.flip()
