# Imports
import pygame
import random
import math

# Initialize pygame
pygame.init()

# Setup screen
screen = pygame.display.set_mode((800, 600))

running = True

# Load images
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invaders")
spaceship = pygame.image.load("spaceship.png")
bg = pygame.image.load("bg.png")
bullet_img = pygame.image.load("bullet.png")

# Player default values
startX = 370
startY = 540
change = 0

# Enemy default values
enemy_img = []
ene_startX = []
ene_startY = []
eneX_change = []
eneY_change = []
ene_num = 6

for i in range(ene_num):
    enemy_img.append(pygame.image.load("art.png"))
    ene_startX.append(random.randint(11, 740))
    ene_startY.append(random.randint(10, 421))
    eneX_change.append(0.3)
    eneY_change.append(20)


# Bullet spawn values
bulletImg = pygame.image.load("bullet.png")
bulletX = startX
bulletY = 540
bulletY_change = 0.3
bullet_state = "ready"

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over font

go_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    go_render = go_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(go_render, (200, 250))


def show_score(x, y):
    score_render = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_render, (x, y))


def player(x, y):
    screen.blit(spaceship, (x, y))


def enemy(x, y):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 8, y - 10))


def checkcollision(ene_startX, ene_startY, startX, startY):
    distance = math.sqrt(
        math.pow(ene_startX - bulletX, 2) + math.pow(ene_startY - bulletY, 2)
    )
    if distance < 33:
        return True
    else:
        return False


# Initialize game loop
while running:

    screen.fill((0, 0, 0))
    # screen.blit(bg, (0, 0))
    # Get events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change = -0.3

            if event.key == pygame.K_RIGHT:
                change = 0.3

            if event.key == pygame.K_SPACE:
                bulletX = startX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change = 0

    # Player Movement
    startX += change

    if startX <= 10:
        startX = 10
    elif startX >= 760:
        startX = 760

    # Enemy Movement
    for i in range(ene_num):
        # GameOver
        if ene_startY[i] > 480:
            for j in range(ene_num):
                ene_startY[j] = 2000
            game_over_text()
            break

        ene_startX[i] += eneX_change[i]

        if ene_startX[i] <= 10:
            eneX_change[i] = 0.1
            ene_startY[i] += eneY_change[i]
        elif ene_startX[i] >= 740:
            eneX_change[i] = -0.1
            ene_startY[i] += eneY_change[i]

        # Collision
        collision = checkcollision(
            ene_startX[i], ene_startY[i], startX, startY)
        if collision:
            bulletY = 540
            bullet_state = "ready"
            score += 1
            ene_startX[i] = random.randint(11, 761)
            ene_startY[i] = random.randint(10, 421)

        enemy(ene_startX[i], ene_startY[i])

    # Bullet
    if bulletY <= 0:
        # bulletX = startX
        bulletY = 540
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(startX, startY)
    show_score(textX, textY)
    pygame.display.update()
