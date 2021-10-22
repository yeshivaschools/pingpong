import json
import types
import random
import math
import pygame

with open("settings.json") as file:
    settings = json.load(file, object_hook=lambda d: types.SimpleNamespace(**d))

pygame.init()

clock = pygame.time.Clock()

game = pygame.display.set_mode((settings.width, settings.height))

pygame.display.set_caption("Pong", "aroary")

width, height = pygame.display.get_surface().get_size()
font = pygame.font.SysFont(None, 50)
editor_font = pygame.font.SysFont(None, math.floor(height / 15))

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

while not close_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_TAB] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
        open_settings = True
        break

    if keys[pygame.K_SPACE]:
        if paused:
            paused = False

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

if open_settings:
    def char_check(data_setting, chars):
        chars = chars.split(",")
        if data_setting == "window" and len(chars) == 2 and chars[0].isnumeric() and chars[1].isnumeric():
            arg1 = int(chars[0])
            arg2 = int(chars[1])
            if arg1 >= 300 and arg1 <= 1200 and arg2 >= 500 and arg2 <= 20000:
                return "green"
        return "red"

    # window settings
    window_input_box = pygame.Rect(width / 3, 5, (width / 3) * 2 - 20, 40)
    window_color_inactive = pygame.Color('lightskyblue3')
    window_color_active = pygame.Color('dodgerblue2')
    window_color = window_color_inactive
    window_text_color = "green"
    window_active = False
    window_text = f"{width},{height}"

    # bot settings
    bot_input_box = pygame.Rect(width / 3, height / 5 + 5, (width / 3) * 2 - 20, 40)
    bot_color_inactive = pygame.Color('lightskyblue3')
    bot_color_active = pygame.Color('dodgerblue2')
    bot_color = bot_color_inactive
    bot_text_color = "green"
    bot_active = False
    bot_text = f"{settings.robotPlayer},{settings.robotView}"

    # ball settings
    ball_input_box = pygame.Rect(width / 3, (height / 5) * 2 + 5, (width / 3) * 2 - 20, 40)
    ball_color_inactive = pygame.Color('lightskyblue3')
    ball_color_active = pygame.Color('dodgerblue2')
    ball_color = ball_color_inactive
    ball_text_color = "green"
    ball_active = False
    ball_text = f"{speed},{radius}"

    # left paddle settings
    p1_input_box = pygame.Rect(width / 3, (height / 5) * 3 + 5, (width / 3) * 2 - 20, 40)
    p1_color_inactive = pygame.Color('lightskyblue3')
    p1_color_active = pygame.Color('dodgerblue2')
    p1_color = p1_color_inactive
    p1_text_color = "green"
    p1_active = False
    p1_text = f"{p1_paddle_width},{p1_paddle_height},{p1_paddle_speed}"

    # right paddle settings
    p2_input_box = pygame.Rect(width / 3, (height / 5) * 4 + 5, (width / 3) * 2 - 20, 40)
    p2_color_inactive = pygame.Color('lightskyblue3')
    p2_color_active = pygame.Color('dodgerblue2')
    p2_color = p2_color_inactive
    p2_text_color = "green"
    p2_active = False
    p2_text = f"{p2_paddle_width},{p2_paddle_height},{p2_paddle_speed}"

    allowed_chars = "0123456789,".split()
    close_settigs = False

    while not close_settigs:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_settigs = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if window_input_box.collidepoint(event.pos):
                    window_active = not window_active
                else:
                    window_active = False
                
                if bot_input_box.collidepoint(event.pos):
                    bot_active = not bot_active
                else:
                    bot_active = False
                
                if ball_input_box.collidepoint(event.pos):
                    ball_active = not ball_active
                else:
                    ball_active = False
                
                if p1_input_box.collidepoint(event.pos):
                    p1_active = not p1_active
                else:
                    p1_active = False
                
                if p2_input_box.collidepoint(event.pos):
                    p2_active = not p2_active
                else:
                    p2_active = False
                
                window_color = window_color_active if window_active else window_color_inactive
                bot_color = bot_color_active if bot_active else bot_color_inactive
                ball_color = ball_color_active if ball_active else ball_color_inactive
                p1_color = p1_color_active if p1_active else p1_color_inactive
                p2_color = p2_color_active if p2_active else p2_color_inactive
            if event.type == pygame.KEYDOWN:
                if window_active:
                    if event.key == pygame.K_RETURN:
                        window_text = window_text
                    elif event.key == pygame.K_BACKSPACE:
                        window_text = window_text[:-1]
                        window_text_color = char_check("window", window_text)
                    else:
                        window_text += event.unicode
                        window_text_color = char_check("window", window_text)

                if bot_active:
                    if event.key == pygame.K_RETURN:
                        bot_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        bot_text = bot_text[:-1]
                    else:
                        bot_text += event.unicode

                if ball_active:
                    if event.key == pygame.K_RETURN:
                        ball_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        ball_text = ball_text[:-1]
                    else:
                        ball_text += event.unicode

                if p1_active:
                    if event.key == pygame.K_RETURN:
                        p1_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        p1_text = p1_text[:-1]
                    else:
                        p1_text += event.unicode

                if p2_active:
                    if event.key == pygame.K_RETURN:
                        p2_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        p2_text = p2_text[:-1]
                    else:
                        p2_text += event.unicode

        game.fill("black")

        game.blit(font.render(window_text, True, window_text_color), (window_input_box.x + 5, window_input_box.y + 5))
        pygame.draw.rect(game, window_color, window_input_box, 2, 4)
        
        game.blit(font.render(bot_text, True, bot_text_color), (bot_input_box.x + 5, bot_input_box.y + 5))
        pygame.draw.rect(game, bot_color, bot_input_box, 2, 4)

        game.blit(font.render(ball_text, True, ball_text_color), (ball_input_box.x + 5, ball_input_box.y + 5))
        pygame.draw.rect(game, ball_color, ball_input_box, 2, 4)

        game.blit(font.render(p1_text, True, p1_text_color), (p1_input_box.x + 5, p1_input_box.y + 5))
        pygame.draw.rect(game, p1_color, p1_input_box, 2, 4)

        game.blit(font.render(p2_text, True, p2_text_color), (p2_input_box.x + 5, p2_input_box.y + 5))
        pygame.draw.rect(game, p2_color, p2_input_box, 2, 4)
        
        pygame.display.flip()
        clock.tick(30)

pygame.quit()