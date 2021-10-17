import json
import sys
import random
import pygame

with open("settings.json") as file:
    settings = json.load(file)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((settings["width"], settings["height"]))
pygame.display.set_caption("Pong", "aroary")
width, height = pygame.display.get_surface().get_size()
font = pygame.font.SysFont("Sans Sheriff", 50)

# Settings
speed = settings["ball"]["speed"]
radius = settings["ball"]["radius"]
p1_paddle_speed = settings["paddle"]["p1"]["speed"]
p1_paddle_width = settings["paddle"]["p1"]["width"]
p1_paddle_height = settings["paddle"]["p1"]["height"]
p2_paddle_speed = settings["paddle"]["p2"]["speed"]
p2_paddle_width = settings["paddle"]["p2"]["width"]
p2_paddle_height = settings["paddle"]["p2"]["height"]

# Positions
serve = 0
p1_position = (height / 2) - (p1_paddle_height / 2)
p2_position = (height / 2) - (p2_paddle_height / 2)
ball_position = [width / 2, height / 2]
ball_x_direction = 0 # 0 for left, 1 for right
ball_y_direction = random.randint(0, 1) # 0 for down, 1 for up

# Score
p1_score = 0
p2_score = 0

# How to play
print('''
player 1:
  w To move up
  s To move Down
player 2:
  up To move up
  down To move Down
''')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            break

    # User motion
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and p2_position >= 0:
        p2_position -= p2_paddle_speed
    if keys[pygame.K_DOWN] and p2_position <= height - p2_paddle_height:
        p2_position += p2_paddle_speed
    if keys[pygame.K_w] and p1_position >= 0:
        p1_position -= p1_paddle_speed
    if keys[pygame.K_s] and p1_position <= height - p1_paddle_height:
        p1_position += p1_paddle_speed

    # Ball motion
    if ball_position[1] == 0:
        ball_y_direction = 0
    if ball_position[1] == height:
        ball_y_direction = 1

    if ball_y_direction:
        ball_position[1] -= speed
    else:
        ball_position[1] += speed

    if ball_x_direction:
        ball_position[0] -= speed
    else:
        ball_position[0] += speed

    if ball_position[0] <= 0:
        p2_score += 1

        ball_y_direction = random.randint(0, 1)
        ball_position = [width / 2, height / 2]

        # Handle serve
        if serve:
            serve = 0
        else:
            serve = 1
        ball_x_direction = serve
    if ball_position[0] >= width:
        p1_score += 1

        ball_y_direction = random.randint(0, 1)
        ball_position = [width / 2, height / 2]

        # Handle serve
        if serve:
            serve = 0
        else:
            serve = 1
        ball_x_direction = serve

    # Handle ball & paddle interaction
    if ball_position[0] <= 5 + p1_paddle_width + radius / 2 and p1_position - radius / 2 <= ball_position[1] and p1_position + p1_paddle_height + radius / 2 >= ball_position[1]:
        ball_x_direction = 0
    if ball_position[0] >= width - 5 - p1_paddle_width - radius / 2 and p2_position - radius / 2 <= ball_position[1] and p2_position + p2_paddle_height + radius / 2 >= ball_position[1]:
        ball_x_direction = 1

    # Board
    screen.fill("black")
    pygame.draw.rect(screen, "white",pygame.Rect(width / 2 - 5, 0, 10, height))
    pygame.draw.circle(screen, "white", (width / 2, height / 2), 100)
    pygame.draw.circle(screen, "black", (width / 2, height / 2), 90)
    pygame.draw.circle(screen, "white", (width / 2, height / 2), 10)

    # Players
    pygame.draw.rect(screen, "white", pygame.Rect(p1_paddle_width, p1_position, 5, 50))
    pygame.draw.rect(screen, "white", pygame.Rect(width - p2_paddle_width * 2, p2_position, 5, 50))

    # Score
    screen.blit(font.render(str(p1_score), False, "white"), (width / 4 - 25, 0))
    screen.blit(font.render(str(p2_score), False, "white"), ((width / 4) * 3 + 10, 0))

    # Ball
    pygame.draw.circle(screen, "yellow", (ball_position[0], ball_position[1]), radius)

    pygame.display.flip()
    clock.tick(60)