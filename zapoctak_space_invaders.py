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

FPS=60

pygame.display.set_caption("Space Invaders by Adam Červenka")
icon1=pygame.image.load("alien1.png")
pygame.display.set_icon(icon1)
background=pygame.image.load("background1.jfif")

score=0
best_score=[score]
direction=0

enemies_count=10
enemiesY_change=50
def new_enemies(enemies_count):
    global enemies,enemiesX,enemiesY,enemiesX_change
    enemies=[]
    enemiesX=[]
    enemiesY=[]
    enemiesX_change=[]
    for _ in range(enemies_count):
        enemies.append(pygame.image.load("alien1.png"))
        enemiesX.append(random.randint(0,width-64))
        enemiesY.append(random.randint(20,height//3))
        enemiesX_change.append(random.choice((-5,5)))
    
    
rocket=pygame.image.load("rocket1.png")
rocketX=width//2
rocketY=height-85
rocketX_change=7

bullet=pygame.image.load("bullet2.png")
bulletX=rocketX
bulletY=rocketY
bulletY_change=18
bullet_fired=False

bombsY_change=5
def new_bombs():
    global bombs,bombs_count,bombsX,bombsY
    bombsX=[]
    bombsY=[]
    bombs=[] 
    bombs_count=0

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
    screen.blit(bullet,(x,y))

def draw_bomb(which,x,y):
    screen.blit(bombs[which],(x,y))

def enemy_bullet_collision(enemyX,enemyY,bulletX,bulletY):
    if bulletX>=enemyX and bulletX+3<=enemyX+64:
        if abs(enemyY-bulletY)<30:
            return True
        else:
            return False
    else:
        return False
    
def rocket_bomb_collision(rocketX,rocketY,bombX,bombY):
    if bombX>=rocketX and bombX+7<=rocketX+40:
        if bombY+10>=rocketY:
            return True
        else:
            return False
    return False
    
def game_over():
    global rocketY,is_game_over,bulletY
    for i in range(enemies_count):
        enemiesY[i]=height+80

    best_score.append(score)
    new_bombs()

    end=text2.render("Game Over",True,white)
    restart=text1.render("Press space to restart the game",True,white)
    best_result=text1.render("Your best score is: "+str(max(i for i in best_score)),True,white)

    screen.blit(end,(width//3.5,height//2.8))
    screen.blit(restart,(width//4.5,height//2.05))
    screen.blit(best_result,(width//3.5,height//1.83))
    if bullet_fired:
        bulletY=-80
    rocketY=-80
    is_game_over=True

def enemies_actions():
    global score, bullet_fired, bulletX, bulletY, bombs_count
    for which in range(enemies_count):
        if enemiesY[which]+40>=rocketY:
            game_over()
            break

        enemiesX[which]+=enemiesX_change[which]
        if enemiesX[which]<0:
            enemiesX_change[which]=-enemiesX_change[which]
            enemiesY[which]+=enemiesY_change

        if enemiesX[which]>width-64:
            enemiesX_change[which]=-enemiesX_change[which]
            enemiesY[which]+=enemiesY_change

        if enemiesX[which]<=rocketX+10 and enemiesX[which]>=rocketX-10:
            a=random.randint(0,100)
            if a>95:
                bombs_count+=1
                bombsX.append(enemiesX[which]+25)
                bombsY.append(enemiesY[which]+10)
                bombs.append(pygame.image.load("bomb1.png"))

        if bullet_fired is True:
            if enemy_bullet_collision(enemiesX[which],enemiesY[which],bulletX,bulletY):
                bullet_fired=False
                bulletY=rocketY
                score+=1
                enemiesX[which]=random.randint(30,width-64)
                enemiesY[which]=random.randint(20,height//2.5)

        draw_enemy(which,enemiesX[which],enemiesY[which])
        

def bombs_actions():
    global bombs_count
    for i in range(bombs_count):  
        if bombs[i] is not None:
            draw_bomb(i,bombsX[i],bombsY[i])
            bombsY[i]+=bombsY_change
            if bombsY[i]>=rocketY+30:
                bombs[i]=None
                
            if rocket_bomb_collision(rocketX,rocketY,bombsX[i],bombsY[i]):
                game_over()
                break

new_enemies(enemies_count)
new_bombs()
is_running=True
is_game_over=False
while is_running:
    screen.fill(black)
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            is_running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                direction=-1
            if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                direction=1
            if event.key==pygame.K_SPACE:
                if is_game_over:
                    score=0
                    new_enemies(enemies_count)
                    is_game_over=False
                    rocketY=height-90
                    
                if bullet_fired is False and is_game_over is False:
                    bullet_fired=True
                    bulletX=rocketX+18
                    
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
    bombs_actions()
    if bullet_fired is True:
        draw_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    if bulletY<=0:
        bullet_fired=False
        bulletY=rocketY
    

    draw_rocket(rocketX,rocketY)
    draw_score(score)
    clock.tick(FPS)
    pygame.display.flip()
