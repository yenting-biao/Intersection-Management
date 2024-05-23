import pygame
import sys
import time
import random
from ControlCenter import ControlCenter
from Map import GameMap
from parameters import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    TILE_SIZE,
    ROWS,
    COLS,
    BLACK,
    GRAY,
    GREEN,
    WHITE,
    RED,
    BLUE,
    PURPLE,
    LIGHT_GREEN,
)
from Car import Car

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(GRAY)
pygame.display.set_caption("Intersection Management Simulation")

# Define the game map
# 0 for roads, 1 for non-accessible areas,
# 2 for horizontal lane lines, 3 for vertical lane lines, 4 for intersection
gameMap = GameMap(screen)

# Create the player car
LEFT_START = (28, 0)
LEFT_END = (26, 0)
TOP_START = (0, 26)
TOP_END = (0, 28)
RIGHT_START = (26, 54)
RIGHT_END = (28, 54)
BOTTOM_START = (54, 28)
BOTTOM_END = (54, 26)

LEFT_COLOR = RED
TOP_COLOR = PURPLE
RIGHT_COLOR = BLUE
BOTTOM_COLOR = LIGHT_GREEN

cars = [
    Car(LEFT_START, TOP_END, screen, gameMap.game_map, RED),
    Car(RIGHT_START, LEFT_END, screen, gameMap.game_map, BLUE),
    # Car(TOP_START, BOTTOM_END, screen, gameMap.game_map, PURPLE),
    # Car(BOTTOM_START, RIGHT_END, screen, gameMap.game_map, LIGHT_GREEN),
]

controller1 = ControlCenter()
controller1.addCar(
    {
        "index": 0,
        "currentPosition": (28, 0),
        "trajectory": [
            (28, 25),
            (28, 26),
            (28, 27),
            (28, 28),
            (27, 28),
            (26, 28),
            (25, 28),
        ],
    }
)

# Main game loop
while True:
    screen.fill(GRAY)

    gameMap.draw()

    # Draw the player car
    for car in cars:
        car.draw()

    if True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    cars[0].move(-1, 0)
                elif event.key == pygame.K_DOWN:
                    cars[0].move(1, 0)
                elif event.key == pygame.K_LEFT:
                    cars[0].move(0, -1)
                elif event.key == pygame.K_RIGHT:
                    cars[0].move(0, 1)
                # print(gameMap.game_map[cars[0].y][cars[0].x])

        # for i in range(1, len(cars)):
        #     dir = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        #     opt = 1  # random.randint(0, 3)
        #     cars[i].move(dir[opt][0], dir[opt][1])
        # Update the display
        pygame.display.flip()
        time.sleep(0.1)

    else:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            cars[0].move(0, -1)
        if keys[pygame.K_DOWN]:
            cars[0].move(0, 1)
        if keys[pygame.K_LEFT]:
            cars[0].move(-1, 0)
        if keys[pygame.K_RIGHT]:
            cars[0].move(1, 0)

        # Update the display
        pygame.display.flip()
