#Space invaders
#Adam Červenka, 1. ročník Bc. studia Informatiky, kruh 37
#zimní semestr 2021/2022
#Programování 1 NPRG030

import math
import random
import pygame

#basic settings
pygame.init()
width=720
height=580
screen=pygame.display.set_mode((width,height))
white=pygame.Color(255,255,255)
clock=pygame.time.Clock()

pygame.display.set_caption("Space Invaders by Adam Červenka")
icon1=pygame.image.load("alien1.png")
pygame.display.set_icon(icon1)     #program icon
background=pygame.image.load("background1.jfif")    #background

#constants
FPS=55              #frames per second
enemies_count=9     #number of enemies
enemies_speed=5     #horizontal velocity of enemies
enemiesY_change=50  #vertical velocity of enemies
rocketX_change=7    #horizontal velocity of rocket
bulletY_change=18   #vertical velocity of rocket
bombsY_change=5     #vertical veloctiy of bombs

score=0
best_score=[]
direction=""

#basic settings of rocket
rocket=pygame.image.load("rocket1.png")
rocketX=width//2
rocketY=height-85

#basic settings of bullet
bullet=pygame.image.load("bullet2.png")
bulletX=rocketX
bulletY=rocketY
bullet_fired=False

#texts
text1=pygame.font.Font("bebas.ttf",30)
text2=pygame.font.Font("bebas.ttf",70)

#generating new enemies
def new_enemies(enemies_count):
    global enemies,enemiesX,enemiesY,enemiesX_change
    enemies=[]
    enemiesX=[]
    enemiesY=[]
    enemiesX_change=[]
    for _ in range(enemies_count):
        enemies.append(pygame.image.load("alien1.png"))
        enemiesX.append(random.randint(0,width-64))
        enemiesY.append(random.randint(20,height//3.5))
        enemiesX_change.append(random.choice((-enemies_speed,enemies_speed)))
    #we get 4 arrays full of information of enemies

#function for generating bombs
def new_bombs():
    global bombs,bombs_count,bombsX,bombsY
    bombsX=[]
    bombsY=[]
    bombs=[] 
    bombs_count=0

#add_bomb is called after some enemy drops bomb
#it adds a bomb to the game
def add_bomb(x,y):
    global bombs,bombs_count,bombsX,bombsY
    bombs_count+=1
    bombsX.append(x+25)
    bombsY.append(y+10)
    bombs.append(pygame.image.load("bomb1.png"))


#functions for drawing
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

#function for collision detection, returns True if a collision happens
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

#function for game ending
def game_over():
    global rocketY,is_game_over,bulletY
    #"deletion" of game objects from the screen
    for i in range(enemies_count):
        enemiesY[i]=height+80
    if bullet_fired:
        bulletY=-80
    rocketY=-80

    best_score.append(score)    #adding score to the best score array
    new_bombs()
    #drawing text Game over and best score
    end=text2.render("Game Over",True,white)
    restart=text1.render("Press space to restart the game",True,white)
    best_result=text1.render("Your best score is: "+str(max(i for i in best_score)),True,white)
    screen.blit(end,(width//3.5,height//2.8))
    screen.blit(restart,(width//4.5,height//2.05))
    screen.blit(best_result,(width//3.5,height//1.83))

    is_game_over=True

#function for enemies actions
def enemies_actions():
    global score, bullet_fired, bulletX, bulletY, bombs_count, enemiesX_change 
    #for all enemies
    for which in range(enemies_count):
        #if enemy is lower than rocket - game over
        if enemiesY[which]+40>=rocketY:
            game_over()
            break

        #bouncing from walls and moving
        enemiesX[which]+=enemiesX_change[which]
        if enemiesX[which]<0:
            enemiesX_change[which]=-enemiesX_change[which]
            enemiesY[which]+=enemiesY_change
        if enemiesX[which]>width-64:
            enemiesX_change[which]=-enemiesX_change[which]
            enemiesY[which]+=enemiesY_change

        #droping bombs, there is a bigger chance to drop a bomb directly onto player
        bomb_likelyhood=random.randint(0,1000) 
        if enemiesX[which]<=rocketX+10 and enemiesX[which]>=rocketX-10: #if an enemy is directly above the rocket
            if bomb_likelyhood>965:     #checking if random number is in an interval
                add_bomb(enemiesX[which],enemiesY[which])
        else:                           #if an enemy is not directly above the rocket
            if bomb_likelyhood>997:
                add_bomb(enemiesX[which],enemiesY[which])

        #if the bullet is fired, we need to check collisions
        if bullet_fired is True:
            #if an enemy is hit, we generate new one and hide bullet
            if enemy_bullet_collision(enemiesX[which],enemiesY[which],bulletX,bulletY):
                bullet_fired=False
                bulletY=rocketY
                score+=1
                enemiesX[which]=random.randint(0,width-64)
                enemiesY[which]=random.randint(20,height//3.5)
                enemiesX_change[which]=random.choice((-enemies_speed,enemies_speed))

        draw_enemy(which,enemiesX[which],enemiesY[which])
        
#function for bomb actions
def bombs_actions():
    global bombs_count
    #for all bombs
    for i in range(bombs_count):
        #None would be, if bomb hadn't hit the rocket
        if bombs[i] is not None:    
            #drawing of bomb
            draw_bomb(i,bombsX[i],bombsY[i])
            bombsY[i]+=bombsY_change
            #bomb didnť hit rocket
            if bombsY[i]>=rocketY+50:   
                bombs[i]=None
            #checking collisions
            if rocket_bomb_collision(rocketX,rocketY,bombsX[i],bombsY[i]):  
                game_over()
                break
            
#function for bullet actions
def bullet_actions():
    global bullet_fired,bulletX,bulletY
    #if bullet is fired, bullet is drawn and is flying upwards
    if bullet_fired is True:
        draw_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
        #checking if bullet isn't outside the screen
        if bulletY<=0:
            bullet_fired=False
            bulletY=rocketY

#initialization of enemies, bombs
new_enemies(enemies_count)
new_bombs()
is_running=True
is_game_over=False

#main game cycle
while is_running:
    screen.blit(background,(0,0))
    #checking keystroke and mouseclick
    for event in pygame.event.get(): 
        #quiting the game
        if event.type==pygame.QUIT:
            is_running=False            
        if event.type==pygame.KEYDOWN:
            #controlling the rocket
            if event.key==pygame.K_LEFT or event.key==pygame.K_a:   
                direction="left"
            if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                direction="right"
            if event.key==pygame.K_SPACE:

                #new game after pressing space
                if is_game_over:        
                    score=0
                    new_enemies(enemies_count)
                    is_game_over=False
                    rocketY=height-90

                #firing a bullet   
                if bullet_fired is False and is_game_over is False:     
                    bullet_fired=True
                    bulletX=rocketX+18

        #stopping the movement after key release
        if event.type==pygame.KEYUP:        
            if event.key==pygame.K_LEFT or event.key==pygame.K_a or event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                direction=""

    #change of rocket position
    if direction=="left":
        rocketX-=rocketX_change
    if direction=="right":
        rocketX+=rocketX_change

    #rocket can't go beyond screen
    if rocketX>=width-40:
        rocketX=width-40
    if rocketX<=0:
        rocketX=0

    #actions of enemies, bombs and bullet
    enemies_actions()
    bombs_actions()
    bullet_actions()
    
    #drawing and tick
    draw_rocket(rocketX,rocketY)
    draw_score(score)
    clock.tick(FPS)
    pygame.display.flip()
