# Simple pygame program
import math
import random
from typing import List
from classes import ter
# Import and initialize the pygame library
import pygame
from pygame import Vector2

from classes import QTree, QBox, Asteroids

pygame.init()
GAME_BOX = [1800, 1200]
COLOR_RGB_WHITE = (255, 255, 255)
COLOR_RGB_BLACK = (0, 0, 0)
COLOR_RGB_GRAY = (125, 125, 125)
COLOR_RGB_LIGHT_BLUE = (64, 128, 255)
COLOR_RGB_GREEN = (0, 200, 64)
COLOR_RGB_YELLOW = (225, 225, 0)
COLOR_RGB_PINK = (230, 50, 230)

# Set up the drawing window
screen = pygame.display.set_mode(GAME_BOX)


def factory(box: [int, int], max_speed, len):
    lAsteroids: List[QBox] = []
    for i in range(0, len+1):
        y = random.randint(-max_speed, max_speed)
        x = (-1 if random.randint(0, 1) == 0 else 1) * math.sqrt(abs(max_speed - y ** 2))
        lAsteroid = Asteroids(random.randint(8, box[0]), random.randint(8, box[1]), Vector2(x, y))
        lAsteroids.append(lAsteroid)
    return lAsteroids


aster: List[Asteroids] = factory(GAME_BOX, 3, 2000)

# Run until the user asks to quit
running = True
r1 = pygame.Rect((150, 90, 100, 75))
clock = pygame.time.Clock()
ser = (0, GAME_BOX[1], GAME_BOX[0], 0)
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 10)


while running:
    clock.tick(100)
    
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill(COLOR_RGB_WHITE)
    r = aster
    k= []
    i = 0
    while True:
        x = aster[i].x
        y = aster[i].y
    # Draw a solid blue circle in the center
        pygame.draw.circle(screen, COLOR_RGB_BLACK, (x, y), 2)
        if x >= GAME_BOX[0] or x <= 0:
            aster[i].speed.x = aster[i].speed.x * (-1)
        if aster[i].y - 1 <= 0 or aster[i].y + 1 >= GAME_BOX[1]:
            aster[i].speed.y = aster[i].speed.y * (-1)
        aster[i].move()
        aster[i].speed = aster[i].speed.rotate(0.5)
        i += 1
        if i >= len(aster) - 1:
            break
    s = []
    tr = QTree(QBox(0, 0, GAME_BOX[0], GAME_BOX[1]), aster)
    tr.get_boxes(tr.root, s, k=k)
    for rect in s:
       pygame.draw.rect(screen, COLOR_RGB_YELLOW, (rect.left, rect.top, rect.width, rect.height), 1)
    text_surface = my_font.render(f'{len(s)}', False, COLOR_RGB_BLACK)
    text_surface2 = my_font.render(f'{ter}, {len(ter)}', False, COLOR_RGB_BLACK)
    screen.blit(text_surface, (20, 300))
    screen.blit(text_surface2, (20, 320))
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
