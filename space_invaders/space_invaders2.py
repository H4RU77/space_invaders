import pygame
from pygame import mixer

import math
import random

# initialize pygame
pygame.init()

# create the screen and add caption
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Haru's Space Invaders")

# icon
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

# background
background = pygame.image.load('background.png')

# sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

def player(x,y):
    screen.blit(playerImg,(x,y))

def show_score(x,y):
    score = font.render("Score: "+str(score_value),True,(255,255,255)) # rgb color  = white
    screen.blit(score,(x,y))

# bullets

bullet_Img = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_Img,(x+16, y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_num = 6

for i in range(enemy_num):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

# game loop
running = True
while running:

    screen.fill((0,0,0))

    # add background image
    screen.blit(background,(0,0))

     
    
    for event in pygame.event.get():
        # close window
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether is right or left OR SPACE
        if event.type == pygame.KEYDOWN:
            #left
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            #right
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            # space
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # get the current X coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        #  IF KEY IS RELEASED WE STOP MOVING
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range (enemy_num):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        enemy(enemyX[i],enemyY[i],i)

        # collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)

    
    
    # BULLET MOVEMENT
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    # add player and score
    player(playerX,playerY)
    show_score(textX, textY)

    pygame.display.update()

# end game
pygame.quit()