import json
import types
import random
import pygame

with open("settings.json") as file:
    settings = json.load(file, object_hook=lambda d: types.SimpleNamespace(**d))

pygame.init()

clock = pygame.time.Clock()

game = pygame.display.set_mode((settings.width, settings.height))

pygame.display.set_caption("Pong", "aroary")

width, height = pygame.display.get_surface().get_size()
font = pygame.font.SysFont("Sans Sheriff", 50)

# Settings
speed = settings.ball.speed
radius = settings.ball.radius
p1_paddle_speed = settings.paddle.p1.speed
p1_paddle_width = settings.paddle.p1.width
p1_paddle_height = settings.paddle.p1.height
p2_paddle_speed = settings.paddle.p2.speed
p2_paddle_width = settings.paddle.p2.width
p2_paddle_height = settings.paddle.p2.height
open_settings = False
close_game = False

# Audio
audio = settings.audio
if audio:
    pygame.mixer.music.load("effects.mp3")
    pygame.mixer.music.set_volume(settings.volume)

# Positions
serve = 0
p1_position = (height / 2) - (p1_paddle_height / 2)
p2_position = (height / 2) - (p2_paddle_height / 2)
ball_position = [width / 2, height / 2]
ball_x_direction = 0  # 0 for left, 1 for right
ball_y_direction = random.randint(0, 1)  # 0 for down, 1 for up
vertical_speed = speed
paused = True

# Score
p1_score = 0
p2_score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game = True

    if close_game:
        break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_TAB] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
        open_settings = True
        break

    if keys[pygame.K_SPACE]:
        if paused:
            paused = False
        # else:
        #     paused = True

    # User motion
    if settings.robotPlayer == 1:
        if ball_position[0] <= width / settings.robotView:
            if p1_position + p1_paddle_height / 2 > ball_position[1] and p1_position > 0:
                p1_position -= p1_paddle_speed
            if p1_position + p1_paddle_height / 2 < ball_position[1] and p1_position + p1_paddle_height < height:
                p1_position += p1_paddle_speed

        if keys[pygame.K_UP] and p2_position >= 0:
            p2_position -= p2_paddle_speed
        if keys[pygame.K_DOWN] and p2_position <= height - p2_paddle_height:
            p2_position += p2_paddle_speed
    elif settings.robotPlayer == 2:
        if ball_position[0] >= width / settings.robotView:
            if p2_position + p2_paddle_height / 2 > ball_position[1] and p2_position > 0:
                p2_position -= p2_paddle_speed
            if p2_position + p2_paddle_height / 2 < ball_position[1] and p2_position + p2_paddle_height < height:
                p2_position += p2_paddle_speed
        
        if keys[pygame.K_w] and p1_position >= 0:
            p1_position -= p1_paddle_speed
        if keys[pygame.K_s] and p1_position <= height - p1_paddle_height:
            p1_position += p1_paddle_speed
    else:
        if keys[pygame.K_UP] and p2_position >= 0:
            p2_position -= p2_paddle_speed
        if keys[pygame.K_DOWN] and p2_position <= height - p2_paddle_height:
            p2_position += p2_paddle_speed

        if keys[pygame.K_w] and p1_position >= 0:
            p1_position -= p1_paddle_speed
        if keys[pygame.K_s] and p1_position <= height - p1_paddle_height:
            p1_position += p1_paddle_speed

    # Ball horizontal movement
    if not paused:
        if ball_y_direction:
            ball_position[1] -= vertical_speed
        else:
            ball_position[1] += vertical_speed

        if ball_x_direction:
            ball_position[0] -= speed
        else:
            ball_position[0] += speed

    # Ball vertical motion
    if ball_position[1] <= radius / 2:
        ball_y_direction = 0
    if ball_position[1] >= height - radius / 2:
        ball_y_direction = 1

    # Handle scoring
    if ball_position[0] <= 0:
        p2_score += 1
        ball_y_direction = random.randint(0, 1)
        ball_position = [width / 2, height / 2]
        vertical_speed = speed
        # Handle serve
        if serve:
            serve = 0
        else:
            serve = 1
        ball_x_direction = serve
        paused = True
    if ball_position[0] >= width:
        p1_score += 1
        ball_y_direction = random.randint(0, 1)
        ball_position = [width / 2, height / 2]
        vertical_speed = speed
        # Handle serve
        if serve:
            serve = 0
        else:
            serve = 1
        ball_x_direction = serve
        paused = True

    # Handle ball & paddle interaction
    if ball_position[0] <= 5 + p1_paddle_width + radius / 2 and p1_position - radius / 2 <= ball_position[1] and p1_position + p1_paddle_height + radius / 2 >= ball_position[1]:
        ball_x_direction = 0
        if ball_position[1] >= p1_position - radius / 2 and ball_position[1] <= p1_position - radius / 2 + 15:
            vertical_speed += 1
            ball_y_direction = 1
        elif ball_position[1] <= p1_position + p1_paddle_height + radius / 2 and ball_position[1] >= p1_position + p1_paddle_height + radius / 2 - 15:
            vertical_speed += 1
            ball_y_direction = 0
        else:
            vertical_speed -= .25
        if audio:
            pygame.mixer.music.play()
    if ball_position[0] >= width - 5 - p2_paddle_width - radius / 2 and p2_position - radius / 2 <= ball_position[1] and p2_position + p2_paddle_height + radius / 2 >= ball_position[1]:
        ball_x_direction = 1
        if ball_position[1] >= p2_position - radius / 2 and ball_position[1] <= p2_position - radius / 2 + 15:
            vertical_speed += 1
            ball_y_direction = 1
        elif ball_position[1] <= p2_position + p2_paddle_height + radius / 2 and ball_position[1] >= p2_position + p2_paddle_height + radius / 2 - 15:
            vertical_speed += 1
            ball_y_direction = 0
        else:
            vertical_speed -= .25
        if audio:
            pygame.mixer.music.play()

    # Board
    game.fill("black")
    pygame.draw.rect(game, "white", pygame.Rect(width / 2 - 5, 0, 10, height))
    pygame.draw.circle(game, "white", (width / 2, height / 2), height / 4)
    pygame.draw.circle(game, "black", (width / 2, height / 2), height / 4 - 10)
    pygame.draw.circle(game, "white", (width / 2, height / 2), 10)

    # Players
    pygame.draw.rect(game, "white", pygame.Rect(5, p1_position, p1_paddle_width, p1_paddle_height), 0, 0, 0, 10, 0, 10)
    pygame.draw.rect(game, "white", pygame.Rect(width - p2_paddle_width - 5, p2_position, p2_paddle_width, p2_paddle_height), 0, 0, 10, 0, 10, 0)

    # Score
    game.blit(font.render(str(p1_score), False, "white"), (width / 4 - 25, 0))
    game.blit(font.render(str(p2_score), False, "white"), ((width / 4) * 3 + 10, 0))

    # Ball
    pygame.draw.circle(game, "grey", (ball_position[0], ball_position[1]), radius)

    pygame.display.flip()
    clock.tick(60)

# replace with a settings editor window
if open_settings:
    data = json.dumps(settings, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    while True:
        game.fill("black")

        format_data = data.split("\n")
        line = 0
        for i in format_data:
            game.blit(font.render(i, False, "white"), (0, line))
            line += 50
        
        pygame.display.flip()
        clock.tick(10)

pygame.quit()