import random
import math
import pygame
from pygame import mixer
pygame.init()


# create the screen
screen = pygame.display.set_mode((800,600))


# Background
background = pygame.image.load("background.png")


# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)


# Title and Icon
pygame.display.set_caption("Space Invaders")


icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)


# Player
player_img = pygame.image.load("player.png")
player_x = 370
player_y = 480
player_x_change = 0

# Player draw function
def player(x, y):
    # blit means draw
    screen.blit(player_img, (x, y))


# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemies = 6

for i in range(num_enemies):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

# Enemy draw function
def enemy(x, y, i):
    # blit means draw
    screen.blit(enemy_img[i], (x, y))


# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 4
bullet_y_change = 20
bullet_state = "ready"

# Bullet draw function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))


# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

text_x = 10
text_y = 10

def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Collision Detection Function
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x-bullet_x, 2) + math.pow(enemy_y-bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # RGB Background
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0,0))



    # event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        # Key pressed
        if event.type == pygame.KEYDOWN:
            # print("Key pressed")
            # check if left or right key is pressed
            if event.key == pygame.K_LEFT:
                player_x_change = -5

            if event.key == pygame.K_RIGHT:
                player_x_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # Play bullet fire sound
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()

                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)


        # Key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0



    # Change player x value
    player_x += player_x_change

    # Restrict the player from going outside the width of the screen
    if player_x <=0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Player draw call
    player(player_x, player_y)


    # Enemy movement
    for i in range(num_enemies):
        if enemy_y[i] > 440:
            for j in range(num_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        # Change enemy x value
        enemy_x[i] += enemy_x_change[i]

        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            # Play explosion sound on collision
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()

            # Reset enemy position
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        # Enemy draw call
        enemy(enemy_x[i], enemy_y[i], i)


    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change


    # Display / render score
    show_score(text_x, text_y)


    pygame.display.update()
