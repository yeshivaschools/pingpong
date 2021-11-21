from random import randint
from math import floor
from json import load, dump
from types import SimpleNamespace
import pygame

pygame.init()

with open("settings.json") as file:
    settings = load(file, object_hook=lambda d: SimpleNamespace(**d))

clock = pygame.time.Clock()

game = pygame.display.set_mode((settings.width, settings.height))

pygame.display.set_caption("Pong", "aroary")

width, height = pygame.display.get_surface().get_size()
font = pygame.font.SysFont(None, 50)
editor_font = pygame.font.SysFont("times", floor(height / 15))

close_game = False
open_settings = False
leave_home = False

start_text = font.render("Play", True, "black")
settings_text = font.render("Settings", True, "black")
start_button = pygame.Rect(width / 2 - settings_text.get_width() / 2, height / 2, settings_text.get_width() + 10, settings_text.get_height() + 10)
settings_button = pygame.Rect(width / 2 - settings_text.get_width() / 2, height / 2 + settings_text.get_height() + 15, settings_text.get_width() + 10, settings_text.get_height() + 10)
while not leave_home:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            leave_home = True
            close_game = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                leave_home = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                leave_home = True
            elif settings_button.collidepoint(event.pos):
                leave_home = True
                close_game = True
                open_settings = True

    game.fill("black")

    game_name = font.render("Pong", True, "white")
    game.blit(game_name, (width / 5 - game_name.get_width() / 2, height / 5))

    pygame.draw.rect(game, "grey" if start_button.collidepoint(pygame.mouse.get_pos()) else "white", start_button, 0, 4)
    game.blit(start_text, (width / 2 - start_text.get_width() / 2 + 5, height / 2 + 5))

    pygame.draw.rect(game, "grey" if settings_button.collidepoint(pygame.mouse.get_pos()) else "white", settings_button, 0, 4)
    game.blit(settings_text, (width / 2 - settings_text.get_width() / 2 + 5, height / 2 + settings_text.get_height() + 20))

    pygame.display.flip()
    clock.tick(10)

speed = settings.ball.speed
radius = settings.ball.radius
p1_paddle_speed = settings.paddle.p1.speed
p1_paddle_width = settings.paddle.p1.width
p1_paddle_height = settings.paddle.p1.height
p2_paddle_speed = settings.paddle.p2.speed
p2_paddle_width = settings.paddle.p2.width
p2_paddle_height = settings.paddle.p2.height

audio = settings.audio
if audio:
    pygame.mixer.music.load("effects.mp3")
    pygame.mixer.music.set_volume(settings.volume)

p1_position = (height / 2) - (p1_paddle_height / 2)
p2_position = (height / 2) - (p2_paddle_height / 2)
ball_position = [width / 2, height / 2]
vertical_speed = speed
paused = True

p1_score = 0
p2_score = 0

while not close_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if paused:
            paused = False

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

    if not paused:
        ball_position[1] += vertical_speed
        ball_position[0] += speed

    if ball_position[1] <= radius / 2 or ball_position[1] >= height - radius / 2:
        vertical_speed *= -1

    if ball_position[0] <= 0 or ball_position[0] >= width:
        ball_position = [width / 2, height / 2]
        vertical_speed = speed
        paused = True
        
        if ball_position[0] <= 0:
            p1_score += 1
        else:
            p2_score += 1

    if ball_position[0] <= 5 + p1_paddle_width + radius / 2 and p1_position - radius / 2 <= ball_position[1] and p1_position + p1_paddle_height + radius / 2 >= ball_position[1] and speed < 0:
        speed *= -1
        if ball_position[1] >= p1_position - radius / 2 and ball_position[1] <= p1_position - radius / 2 + 15 and vertical_speed > 0:
            vertical_speed = vertical_speed * -1 + 1
        elif ball_position[1] <= p1_position + p1_paddle_height + radius / 2 and ball_position[1] >= p1_position + p1_paddle_height + radius / 2 - 15 and vertical_speed < 0:
            vertical_speed = vertical_speed * -1 - 1
        else:
            vertical_speed -= .25
        if audio:
            pygame.mixer.music.play()
    if ball_position[0] >= width - 5 - p2_paddle_width - radius / 2 and p2_position - radius / 2 <= ball_position[1] and p2_position + p2_paddle_height + radius / 2 >= ball_position[1] and speed > 0:
        speed *= -1
        if ball_position[1] >= p2_position - radius / 2 and ball_position[1] <= p2_position - radius / 2 + 15 and vertical_speed > 0:
            vertical_speed = vertical_speed * -1 + 1
        elif ball_position[1] <= p2_position + p2_paddle_height + radius / 2 and ball_position[1] >= p2_position + p2_paddle_height + radius / 2 - 15 and vertical_speed < 0:
            vertical_speed = vertical_speed * -1 - 1
        else:
            vertical_speed += .25
        if audio:
            pygame.mixer.music.play()

    game.fill("black")
    pygame.draw.rect(game, "white", pygame.Rect(width / 2 - 5, 0, 10, height))
    pygame.draw.circle(game, "white", (width / 2, height / 2), height / 4)
    pygame.draw.circle(game, "black", (width / 2, height / 2), height / 4 - 10)
    pygame.draw.circle(game, "white", (width / 2, height / 2), 10)

    pygame.draw.rect(game, "white", pygame.Rect(5, p1_position, p1_paddle_width, p1_paddle_height), 0, 0, 0, 10, 0, 10)
    pygame.draw.rect(game, "white", pygame.Rect(width - p2_paddle_width - 5, p2_position, p2_paddle_width, p2_paddle_height), 0, 0, 10, 0, 10, 0)

    game.blit(font.render(str(p1_score), False, "white"), (width / 4 - 25, 0))
    game.blit(font.render(str(p2_score), False, "white"), ((width / 4) * 3 + 10, 0))

    pygame.draw.circle(game, "grey", (ball_position[0], ball_position[1]), radius)

    pygame.display.flip()
    clock.tick(60)

if open_settings:
    inputs = [
        { "type": "window", "text": f"{width},{height}", "description": [ "w", "h" ] },
        { "type": "robot", "text": f"{settings.robotPlayer},{settings.robotView}", "description": [ "p", "v" ] },
        { "type": "ball", "text": f"{speed},{radius}", "description": [ "s", "r" ] },
        { "type": "p1", "text": f"{p1_paddle_width},{p1_paddle_height},{p1_paddle_speed}", "description": [ "w", "h", "s" ] },
        { "type": "p2", "text": f"{p2_paddle_width},{p2_paddle_height},{p2_paddle_speed}", "description": [ "w", "h", "s" ] }
    ]

    input_settings = {}

    line = 0
    for i in inputs:
        input_settings[i["type"]] = {
            "input_box": pygame.Rect(width / 3, (height / 5) * line + 5, (width / 3) * 2 - 20, 40),
            "color_inactive": pygame.Color('lightskyblue3'),
            "color_active": pygame.Color('dodgerblue2'),
            "color": pygame.Color('lightskyblue3'),
            "text_color": "green",
            "active": False,
            "text": i["text"],
            "description": ",".join(i["description"])
        }

        line += 1

    setting_constraints = {
        "window": [[500, 20000], [300, 1200]],
        "robot": [[0, 2], [1, 3]],
        "ball": [[0, 12], [2, 400]],
        "p1": [[1, 250], [1, 500], [1, 50]],
        "p2": [[1, 250], [1, 500], [1, 50]]
    }

    def char_check(data_setting, chars):
        if chars:
            chars = list(map(int, chars.strip(",").split(",")))
            if data_setting in setting_constraints:
                line = 0
                for i in setting_constraints[data_setting]:
                    if len(chars) > line:
                        if chars[line] < i[0] or chars[line] > i[1]:
                            return "red"
                    else:
                        return "yellow"
                    line += 1
                return "green"
            else:
                return "yellow"
        else:
            return "red"

    allowed_chars = [ pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_COMMA, pygame.K_BACKSPACE ]

    close_settigs = False

    while not close_settigs:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("settings.json", "w") as file:
                    if input_settings["window"]["text_color"] == "green":
                        settings.width, settings.height = list(map(int, input_settings["window"]["text"].split(",")))
                    if input_settings["robot"]["text_color"] == "green":
                        settings.robotPlayer, settings.robotView = list(map(int, input_settings["robot"]["text"].split(",")))
                    if input_settings["ball"]["text_color"] == "green":
                        settings.ball.speed, settings.ball.radius = list(map(int, input_settings["ball"]["text"].split(",")))
                    if input_settings["p1"]["text_color"] == "green":
                        settings.paddle.p1.width, settings.paddle.p1.height, settings.paddle.p1.speed = list(map(int, input_settings["p1"]["text"].split(",")))
                    if input_settings["p2"]["text_color"] == "green":
                        settings.paddle.p2.width, settings.paddle.p2.height, settings.paddle.p2.speed = list(map(int, input_settings["p2"]["text"].split(",")))

                    dump(settings, file, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)
                close_settigs = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in input_settings:
                    if input_settings[i]["input_box"].collidepoint(event.pos):
                        input_settings[i]["active"] = not input_settings[i]["active"]
                    else:
                        input_settings[i]["active"] = False

                    input_settings[i]["color"] = input_settings[i]["color_active"] if input_settings[i]["active"] else input_settings[i]["color_inactive"]

            if event.type == pygame.KEYDOWN and event.key in allowed_chars:
                for i in input_settings:
                    if input_settings[i]["active"]:
                        if event.key == pygame.K_BACKSPACE:
                            input_settings[i]["text"] = input_settings[i]["text"][:-1]
                        else:
                            input_settings[i]["text"] += event.unicode

                        input_settings[i]["text_color"] = char_check(i, input_settings[i]["text"])

        game.fill("black")
        
        line = 0
        for i in input_settings:
            game.blit(font.render(input_settings[i]["text"], True, input_settings[i]["text_color"]), (input_settings[i]["input_box"].x + 5, input_settings[i]["input_box"].y + 5))
            pygame.draw.rect(game, input_settings[i]["color"], input_settings[i]["input_box"], 2, 4)

            game.blit(editor_font.render(i, True, "white"), (5, input_settings[i]["input_box"].y + 5))
            game.blit(editor_font.render(input_settings[i]["description"], True, "white"), (5, input_settings[i]["input_box"].y + editor_font.get_height() + 5))
            line += 1

        pygame.display.flip()
        clock.tick(30)

pygame.quit()
