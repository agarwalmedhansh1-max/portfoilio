import math
import random
import pygame

screen_width, screen_height = 800, 500
player_start_y, player_start_x = 380, 370
enemy_y_min, enemy_y_max= 50, 150
speed_x, speed_y = 4, 40
bullet_speed_y= 10
collision_distance=27

pygame.init()
pygame.mixer.init()

explosion=pygame.mixer.Sound("C:/medhansh/python/advanced/pygame/images and stuff/dragon-studio-loud-explosion-sound-425458.mp3")
screen= pygame.display.set_mode((screen_width, screen_height))
 
bg=pygame.image.load('C:/medhansh/python/advanced/pygame/images and stuff/background.png')
caption=pygame.display.set_caption("Space Invader")
icon=pygame.image.load('C:/medhansh/python/advanced/pygame/images and stuff/UFO.png')
pygame.display.set_icon(icon)

playerimg=pygame.image.load('C:/medhansh/python/advanced/pygame/images and stuff/Player.png')
player_x=player_start_x
player_y=player_start_y

playerx_change=0

#enemy

enemyimg=[]
enemyx=[]
enemyy=[]
enemyx_change=[]
enemyy_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('C:/medhansh/python/advanced/pygame/images and stuff/Enemy.png'))
    enemyx.append(random.randint(0, screen_width-64))
    enemyy.append(random.randint(enemy_y_min, enemy_y_max))
    enemyx_change.append(speed_x)
    enemyy_change.append(speed_y)

#bullet

bulletimg=pygame.image.load('C:/medhansh/python/advanced/pygame/images and stuff/Bullet.png')
bulletx=0
bullety=player_start_y
bulletx_change=0
bullety_change=bullet_speed_y
bullet_state='ready'

#score

score_value=0
font=pygame.font.Font('freesansbold.ttf', 64)
textx=10
texty=10

#game over text

over_font=pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score=font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletimg, (x+16,y+10))

def iscollision(enemyx, enemyy, bulletx, bullety):
    distance=math.sqrt((enemyx-bulletx) **2 + (enemyy - bullety) **2)
    return distance < collision_distance

running = True
while running:
    screen.fill((0,0,0))
    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerx_change=-5
            if event.key==pygame.K_RIGHT:
                playerx_change=5
            if event.key==pygame.K_SPACE and bullet_state=='ready':
                bulletx=player_x
                fire_bullet(bulletx, bullety)
        if event.type==pygame.KEYUP and event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            playerx_change = 0
    player_x += playerx_change
    player_x = max(0, min(player_x, screen_width-64))

    for i in range(num_of_enemies):
        if enemyy[i]>340:
            for j in range(num_of_enemies):
                enemyy[j]=2000
            game_over_text()
            break
        enemyx[i] += enemyx_change[i]
        if enemyx[i]<=0 or enemyx[i]>=screen_width-64:
            enemyx_change[i]*=-1
            enemyy[i]+=enemyy_change[i]
        if iscollision(enemyx[i], enemyy[i], bulletx, bullety):
            explosion.set_volume(0.5)
            explosion.play()
            bullety = player_start_y
            bullet_state=='ready'
            score_value+=1
            speed_x+=1
            enemyx[i]=random.randint(0, screen_width-64)
            enemyy[i]=random.randint(enemy_y_min, enemy_y_max)
        enemy(enemyx[i], enemyy[i], i)
    if bullety<=0:
        bullety=player_start_y
        bullet_state='ready'
    elif bullet_state=='fire':
        fire_bullet(bulletx, bullety)
        bullety-=bullety_change

    player(player_x, player_y)
    show_score(textx,texty)
    pygame.display.update()