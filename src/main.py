import pygame
import sys
import random
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
    YELLOW,
    RED,
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

print("ROWS: ", ROWS)
print("COLS: ", COLS)

# Create the player car
cars = [Car(1, 3, screen, gameMap.game_map) for _ in range(4)]

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
                    cars[0].move(0, -1)
                elif event.key == pygame.K_DOWN:
                    cars[0].move(0, 1)
                elif event.key == pygame.K_LEFT:
                    cars[0].move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    cars[0].move(1, 0)
                print(gameMap.game_map[cars[0].y][cars[0].x])

        for i in range(1, len(cars)):
            dir = [[0, -1], [0, 1], [-1, 0], [1, 0]]
            opt = random.randint(0, 3)
            cars[i].move(dir[opt][0], dir[opt][1])
        # Update the display
        pygame.display.flip()

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
