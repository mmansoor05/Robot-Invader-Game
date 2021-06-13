import pygame
import random

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))  # width, height

# Background
backgroundImg = pygame.image.load('background.png')

# Title and Icon
pygame.display.set_caption("Shooting Monkey")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Monkey
monkeyImg = pygame.image.load('monkey.png')
monkeyImg = pygame.transform.scale(monkeyImg, (90, 90))

monkeyX = 370
monkeyY = 480
monkeyX_change = 0
monkeyY_change = 0

# Robot
robotImg = []
robotX = []
robotY = []
robotX_change = []
robotY_change = []
num_of_robots = 7

for num in range(num_of_robots):
    robotImg.append(pygame.image.load('robot2.png'))
    robotX.append(random.randint(0, 700))
    robotY.append(random.randint(50, 150))
    robotX_change.append(0.3)
    robotY_change.append(20)

# Banana
# Ready - You can't see the banana on the screen
# Fire - Banana is currently moving
bananaImg = pygame.image.load('banana.png')
bananaImg = pygame.transform.scale(bananaImg,(50,50))

bananaX = 0
bananaY = 480
bananaX_change = 0
bananaY_change = 1
banana_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 60)

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def monkey(x, y):
    screen.blit(monkeyImg,(x, y))

def robot(x, y, num):
    screen.blit(robotImg[num], (x, y))

def fire_banana(x,y):
    global banana_state
    banana_state = "fire"
    screen.blit(bananaImg, (x + 30, y + 10))

def is_collision(robotX, robotY, bananaX, bananaY):
    dist = ((robotX - bananaX) ** 2) + ((robotY - bananaY) ** 2)
    total_distance = dist ** 0.5
    if total_distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    # background screen color
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed, check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                monkeyX_change = -0.2
            if event.key == pygame.K_RIGHT:
                monkeyX_change = 0.2
            if event.key == pygame.K_UP:
                monkeyY_change = -0.3
            if event.key == pygame.K_DOWN:
                monkeyY_change = 0.3
            if event.key == pygame.K_SPACE:
                if banana_state == "ready":
                    bananaX = monkeyX
                    fire_banana(bananaX, bananaY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                monkeyX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                monkeyY_change = 0

    # Monkey Movement
    monkeyX += monkeyX_change
    # checking so that monkey does not go out the board
    if monkeyX <= 0:
        monkeyX = 0
    elif monkeyX >= 700:
        monkeyX = 700
    monkeyY += monkeyY_change
    if monkeyY <= 0:
        monkeyY = 0
    elif monkeyY >= 500:
        monkeyY = 500

    # Robot Movement
    for num in range(num_of_robots):
        # Game Over
        if robotY[num] > 420:
            for j in range(num_of_robots):
                robotY[j] = 2000
            game_over_text()
            break

        robotX[num] += robotX_change[num]
        # checking so that robot does not go out the board
        if robotX[num] <= 0:
            robotX_change[num] = 0.3
            robotY[num] += robotY_change[num]
        elif robotX[num] >= 700:
            robotX_change[num] = -0.3
            robotY[num] += robotY_change[num]

        # Collision
        collision = is_collision(robotX[num], robotY[num], bananaX, bananaY)
        if collision:
            bananaY = monkeyY
            banana_state = "ready"
            score_value += 1
            robotX[num] = random.randint(0, 700)
            robotY[num] = random.randint(50, 150)

        robot(robotX[num], robotY[num], num)
    # Banana Movement
    if bananaY <= 0:
        bananaY = monkeyY
        banana_state = "ready"
    if banana_state == "fire":
        fire_banana(bananaX, bananaY)
        bananaY -= bananaY_change

    monkey(monkeyX, monkeyY)
    show_score(textX, textY)
    pygame.display.update()






