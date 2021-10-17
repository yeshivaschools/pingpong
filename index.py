import json
import sys
import pygame

with open("settings.json") as file:
    settings = json.load(file)

print(settings)

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Pong")

width, height = pygame.display.get_surface().get_size()

screen.fill("black")

speed = 2

p1_position = (height / 2) - (50 / 2)
p2_position = (height / 2) - (50 / 2)

p1 = pygame.Rect(5, p1_position, 5, 50)
p2 = pygame.Rect(width - 10, p2_position, 5, 50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and p2_position >= 50:
        p2_position += speed
    if keys[pygame.K_DOWN] and p2_position <= height - 50:
        p2_position -= speed
    if keys[pygame.K_w] and p1_position >= 50:
        p1_position += speed
    if keys[pygame.K_w] and p1_position <= height - 50:
        p1_position -= speed
    
    pygame.display.flip()
    clock.tick(60)

    # board
    pygame.draw.rect(screen, "white",pygame.Rect(width / 2 - 5, 0, 10, height))

    # players
    pygame.draw.rect(screen, "white", p1)
    pygame.draw.rect(screen, "white", p2)