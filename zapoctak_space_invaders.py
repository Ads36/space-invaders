#Space invaders
#Adam Červenka, 1. ročník Bc. studia Informatiky, kruh 37
#zimní semestr 2021/2022
#Programování 1 NPRG030

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
pygame.display.set_icon(icon1)     #ikonka programu
background=pygame.image.load("background1.jfif")    #pozadí

#konstanty
FPS=60              #snímky za sekundu
enemies_count=9     #počet nepřátel
enemies_speed=5     #x-ová rychlost nepřátel
enemiesY_change=50  #y-ový posun nepřátel
rocketX_change=7    #x-ová rychlost rakety
bulletY_change=18   #y-ová rychlost střely
bombsY_change=5     #y-ová rychlost bomby

score=0
best_score=[]
direction=""

#počáteční nastavení rakety
rocket=pygame.image.load("rocket1.png")
rocketX=width//2
rocketY=height-85

#počáteční nastavení střely
bullet=pygame.image.load("bullet2.png")
bulletX=rocketX
bulletY=rocketY
bullet_fired=False

#texty
text1=pygame.font.Font("bebas.ttf",30)
text2=pygame.font.Font("bebas.ttf",70)

#generování nových nepřátel
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
        #získám 4 pole plná údajů o nepřátelích, na jejich základě poté generuji nepřátele

#funkce na generování bomb, new_bombs vytvoří pouze prádzná pole pro údaje o bombách
def new_bombs():
    global bombs,bombs_count,bombsX,bombsY
    bombsX=[]
    bombsY=[]
    bombs=[] 
    bombs_count=0
#add_bomb se volá po dropnutí bomby, přidá bombu do hry
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

#funkce na řešení kolizí, vrací True pokud dojde ke kolizi
def enemy_bullet_collision(enemyX,enemyY,bulletX,bulletY):
    #příčítám 3 a 64 kvůli velikosti střely a nepřátel
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

    best_score.append(score)    #přídání score do pole nejlepších skóre
    new_bombs()
    #vykreslení textu Game over a nejlepšího skóre
    end=text2.render("Game Over",True,white)
    restart=text1.render("Press space to restart the game",True,white)
    best_result=text1.render("Your best score is: "+str(max(i for i in best_score)),True,white)
    screen.blit(end,(width//3.5,height//2.8))
    screen.blit(restart,(width//4.5,height//2.05))
    screen.blit(best_result,(width//3.5,height//1.83))

    is_game_over=True

#funkce pro akce nepřátel
def enemies_actions():
    global score, bullet_fired, bulletX, bulletY, bombs_count, enemiesX_change 
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

        #dropování bomb, je větší šance že bomba spadne přímo na raketu - aby se hráč musel hýbat
        bomb_likelyhood=random.randint(0,1000)  #náhodné číslo
        if enemiesX[which]<=rocketX+10 and enemiesX[which]>=rocketX-10: #pokud je nepřítel nad raketou
            if bomb_likelyhood>965:     #kontroluji jestli náhodné číslo je větší než určitá mez pro dropnutí bomby
                add_bomb(enemiesX[which],enemiesY[which])
        else:       #pokud nepřítel není nad raketou
            if bomb_likelyhood>997:
                add_bomb(enemiesX[which],enemiesY[which])
        #pokud je vystřeleno, tak kontroluji kolize střely a nepřátel
        if bullet_fired is True:
            #pokud je nepřítel sestřelen, tak vygeneruji nového a střelu schovám
            if enemy_bullet_collision(enemiesX[which],enemiesY[which],bulletX,bulletY):
                bullet_fired=False
                bulletY=rocketY
                score+=1
                enemiesX[which]=random.randint(0,width-64)
                enemiesY[which]=random.randint(20,height//3)
                enemiesX_change[which]=random.choice((-enemies_speed,enemies_speed))

        draw_enemy(which,enemiesX[which],enemiesY[which])
        
#funkce pro akce bomb
def bombs_actions():
    global bombs_count
    #akce se provede pro všechny bomby
    for i in range(bombs_count):
        #None by bylo pokud bomba netrefila raketu a propadla pod okno
        if bombs[i] is not None:    
            #vykreslení bomby
            draw_bomb(i,bombsX[i],bombsY[i])
            bombsY[i]+=bombsY_change
            #bomba netrefila raketu
            if bombsY[i]>=rocketY+50:   
                bombs[i]=None
            #kontrola kolize, pokud ano, game over    
            if rocket_bomb_collision(rocketX,rocketY,bombsX[i],bombsY[i]):  
                game_over()
                break
            
#funkce pro akce střely
def bullet_actions():
    global bullet_fired,bulletX,bulletY
    #pokud vystřeleno, tak se kreslí střela a letí nahoru
    if bullet_fired is True:
        draw_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
        #kontrola jestli střela nevyletěla mimo
        if bulletY<=0:
            bullet_fired=False
            bulletY=rocketY

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
        #vypnutí, po stisu křížku   
        if event.type==pygame.QUIT:
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

    #změna pozice rakety v závislosti na ovládání
    if direction=="left":
        rocketX-=rocketX_change
    if direction=="right":
        rocketX+=rocketX_change

    #nemožnost rakety dosáhnout pozice mimo okno
    if rocketX>=width-40:
        rocketX=width-40
    if rocketX<=0:
        rocketX=0

    #akce nepřátel, bomb a střely
    enemies_actions()
    bombs_actions()
    bullet_actions()
    
    #vykreslení a tick
    draw_rocket(rocketX,rocketY)
    draw_score(score)
    clock.tick(FPS)
    pygame.display.flip()
