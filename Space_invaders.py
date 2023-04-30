import math
import random

import pygame

# Initialize Pygame
pygame.init()



# Create the screen
screen = pygame.display.set_mode((1040, 800))

# Set the title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Load the background image
background = pygame.image.load("background.png")



# Load the player image and set its initial position
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0


# Load the enemy image and set its initial position
enemyImg = pygame.image.load("enemy.png")
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change = 4
enemyY_change = 40



# Load the bullet image and set its initial state
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Load the font objects for the score and game over text
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


# Load the sound effects
bullet_sound = pygame.mixer.Sound("laser.wav")
background_music = pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

# Define functions

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
score = 0
running = True
while running:
    # Fill the screen with the background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for key presses to move the player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = pygame.mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # Check for key releases to stop moving the player
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Move the player
    playerX += playerX_change

    # Add boundaries to the player's movement
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Move the enemy
    enemyX += enemyX_change

    # Add boundaries to the enemy's movement and change its direction
    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -4
        enemyY += enemyY_change

    # Move the bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    # Check for collisions
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        score += 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)



##
    # Draw the player, enemy, and score text
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (textX, textY))

    # Check for game over
    if enemyY > 440:
        game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game_over_text, (200, 250))
        running = False




    # Update the display
    pygame.display.update()

