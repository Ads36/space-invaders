import math
import random
import pygame

#základní nastavování
pygame.init()
width=720
height=580
screen=pygame.display.set_mode((width,height))
white=pygame.Color(255,255,255)
clock=pygame.time.Clock()

pygame.display.set_caption("Space Invaders by Adam Červenka")
icon1=pygame.image.load("alien1.png")
pygame.display.set_icon(icon1)
background=pygame.image.load("background1.jfif")

#konstanty
FPS=60
enemies_count=9
enemies_speed=5
enemiesY_change=50
rocketX_change=7
bulletY_change=18
bombsY_change=5

score=0
best_score=[score]
direction=""

#generování nepřátel
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
        enemiesX_change.append(random.choice((-enemies_speed,enemies_speed)))

#počáteční nastavení rakety a náboje
rocket=pygame.image.load("rocket1.png")
rocketX=width//2
rocketY=height-85

bullet=pygame.image.load("bullet2.png")
bulletX=rocketX
bulletY=rocketY
bullet_fired=False

#texty
text1=pygame.font.Font("bebas.ttf",30)
text2=pygame.font.Font("bebas.ttf",70)

#funkce na generování bomb
def new_bombs():
    global bombs,bombs_count,bombsX,bombsY
    bombsX=[]
    bombsY=[]
    bombs=[] 
    bombs_count=0
def add_bomb(x,y):
    global bombs,bombs_count,bombsX,bombsY
    bombs_count+=1
    bombsX.append(x+25)
    bombsY.append(y+10)
    bombs.append(pygame.image.load("bomb1.png"))


#funkce na vykreslování
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

#funkce na řešení kolizí
def enemy_bullet_collision(enemyX,enemyY,bulletX,bulletY):
    #příčítám 3 a 64 kvůli velikosti náboje a nepřátel
    if bulletX>=enemyX and bulletX+3<=enemyX+64:
        if abs(enemyY-bulletY)<30:
            return True
        else:
            return False
    else:
        return False
def rocket_bomb_collision(rocketX,rocketY,bombX,bombY):
    #přičítám 7 a 40 kvůli velikosti bomby a rakety
    if bombX>=rocketX and bombX+7<=rocketX+40:
        if bombY+10>=rocketY:
            return True
        else:
            return False
    return False

#funkce na konec hry
def game_over():
    global rocketY,is_game_over,bulletY
    #"zmizení" herních objektů ze screenu
    for i in range(enemies_count):
        enemiesY[i]=height+80
    if bullet_fired:
        bulletY=-80
    rocketY=-80

    best_score.append(score)
    new_bombs()
    #text Game over a skóre
    end=text2.render("Game Over",True,white)
    restart=text1.render("Press space to restart the game",True,white)
    best_result=text1.render("Your best score is: "+str(max(i for i in best_score)),True,white)
    screen.blit(end,(width//3.5,height//2.8))
    screen.blit(restart,(width//4.5,height//2.05))
    screen.blit(best_result,(width//3.5,height//1.83))

    is_game_over=True

#funkce pro akce nepřátel
def enemies_actions():
    global score, bullet_fired, bulletX, bulletY, bombs_count
    #akce se provede pro všechny nepřátele
    for which in range(enemies_count):
        #pokud nepřítel dosáhl úrovně rakety - game over
        if enemiesY[which]+40>=rocketY:
            game_over()
            break

        #pohyb nepřátel a odrážení od stěn
        enemiesX[which]+=enemiesX_change[which]
        if enemiesX[which]<0:
            enemiesX_change[which]=-enemiesX_change[which]
            enemiesY[which]+=enemiesY_change
        if enemiesX[which]>width-64:
            enemiesX_change[which]=-enemiesX_change[which]
            enemiesY[which]+=enemiesY_change

        #dropování bomb, je větší šance že bomba spadne na hráče - aby se hráč musel hýbat
        bomb_likelyhood=random.randint(0,1000)
        if enemiesX[which]<=rocketX+10 and enemiesX[which]>=rocketX-10:
            if bomb_likelyhood>960:
                add_bomb(enemiesX[which],enemiesY[which])
        else:
            if bomb_likelyhood>997:
                add_bomb(enemiesX[which],enemiesY[which])
        #pokud je vystřeleno tak kontroluji kolize náboje a nepřátel
        if bullet_fired is True:
            #pokud je nepřítel sestřelen, tak vygeneruji nového
            if enemy_bullet_collision(enemiesX[which],enemiesY[which],bulletX,bulletY):
                bullet_fired=False
                bulletY=rocketY
                score+=1
                enemiesX[which]=random.randint(0,width-64)
                enemiesY[which]=random.randint(20,height//3)

        draw_enemy(which,enemiesX[which],enemiesY[which])
        

def bombs_actions():
    global bombs_count
    for i in range(bombs_count):
        #None by bylo pokud bomba netrefila raketu  
        if bombs[i] is not None:    
            draw_bomb(i,bombsX[i],bombsY[i])
            bombsY[i]+=bombsY_change
            #bomba netrefila raketu
            if bombsY[i]>=rocketY+50:   
                bombs[i]=None
            #kontrola kolize, pokud ano, game over    
            if rocket_bomb_collision(rocketX,rocketY,bombsX[i],bombsY[i]):  
                game_over()
                break

#inicializace nepřátel, bomb, běhu hry
new_enemies(enemies_count)
new_bombs()
is_running=True
is_game_over=False

#hlavní chod hry
while is_running:
    screen.blit(background,(0,0))
    #zjištění stisku kláves
    for event in pygame.event.get():    
        if event.type==pygame.QUIT:
            #vypnutí, křížek
            is_running=False            
        if event.type==pygame.KEYDOWN:
            #ovládání
            if event.key==pygame.K_LEFT or event.key==pygame.K_a:   
                direction="left"
            if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                direction="right"
            if event.key==pygame.K_SPACE:

                #nová hra po stisknutí mezerníku
                if is_game_over:        
                    score=0
                    new_enemies(enemies_count)
                    is_game_over=False
                    rocketY=height-90

                #vystřelení    
                if bullet_fired is False and is_game_over is False:     
                    bullet_fired=True
                    bulletX=rocketX+18

        #přerušení pohybu po vymáčknutí klávesy            
        if event.type==pygame.KEYUP:        
            if event.key==pygame.K_LEFT or event.key==pygame.K_a or event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                direction=""

    #změna pozice rakety
    if direction=="left":
        rocketX-=rocketX_change
    if direction=="right":
        rocketX+=rocketX_change

    #nemožnost rakety dosáhnout pozice mimo okno
    if rocketX>=width-40:
        rocketX=width-40
    if rocketX<=0:
        rocketX=0

    #ovládání nepřátel a bomb
    enemies_actions()
    bombs_actions()

    #pokud vystřeleno, tak se kreslí střela a letí
    if bullet_fired is True:
        draw_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    #kontrola jestli střela nevyletěla mimo
    if bulletY<=0:
        bullet_fired=False
        bulletY=rocketY

    #vykreslení a tick
    draw_rocket(rocketX,rocketY)
    draw_score(score)
    clock.tick(FPS)
    pygame.display.flip()
