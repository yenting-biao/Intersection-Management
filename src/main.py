import pygame
import sys
import time
from ControlCenter import ControlCenter
from Map import GameMap
from parameters import (
    ROAD_WIDTH,
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


def generateTrajectory(car: Car, controller: ControlCenter, game_map: list[list[int]]):
    trajectory = []
    dc = controller.center[1] - car.c
    dr = controller.center[0] - car.r
    if abs(dc) < abs(dr):  # move vertically
        curr = (car.r, car.c)
        while game_map[curr[0]][curr[1]] != 4:
            curr = (curr[0] + 1 if dr > 0 else curr[0] - 1, curr[1])

        # trajectory enters intersection
        dc = car.destination[1] - curr[1]
        dr = car.destination[0] - curr[0]
        while game_map[curr[0]][curr[1]] == 4 and curr[0] != car.destination[0]:
            trajectory.append(curr)
            curr = (curr[0] + 1 if dr > 0 else curr[0] - 1, curr[1])
        while game_map[curr[0]][curr[1]] == 4 and curr[1] != car.destination[1]:
            trajectory.append(curr)
            curr = (curr[0], curr[1] + 1 if dc > 0 else curr[1] - 1)
    else:  # move horizontally
        curr = (car.r, car.c)
        while game_map[curr[0]][curr[1]] != 4:
            curr = (curr[0], curr[1] + 1 if dc > 0 else curr[1] - 1)

        # trajectory enters intersection
        dc = car.destination[1] - curr[1]
        dr = car.destination[0] - curr[0]
        while game_map[curr[0]][curr[1]] == 4 and curr[1] != car.destination[1]:
            trajectory.append(curr)
            curr = (curr[0], curr[1] + 1 if dc > 0 else curr[1] - 1)
        while game_map[curr[0]][curr[1]] == 4 and curr[0] != car.destination[0]:
            trajectory.append(curr)
            curr = (curr[0] + 1 if dr > 0 else curr[0] - 1, curr[1])
    return trajectory


def main():

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

    # Main game loop
    while True:
        screen.fill(GRAY)

        gameMap.draw()

        # Draw the player car
        for car in cars:
            car.draw()

        controller1 = ControlCenter((27, 27))
        for i in range(len(cars)):
            # print(cars[i].r, cars[i].c)
            dc = controller1.center[1] - cars[i].c
            dr = controller1.center[0] - cars[i].r
            if abs(dc) + abs(dr) > int(ROAD_WIDTH * 2):
                # far from intersection, keep going
                if abs(dc) < abs(dr):  # move vertically
                    cars[i].move(1 if dr > 0 else -1, 0)
                else:  # move horizontally
                    cars[i].move(0, 1 if dc > 0 else -1)
            else:
                # near intersection, need to call control center
                trajectory = generateTrajectory(cars[i], controller1, gameMap.game_map)
                print("trajectory", trajectory)
                controller1.addCar({"index": i, "trajectory": trajectory})

        controller1.schedule()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # if True:
        #     # Event handling
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             sys.exit()
        #         elif event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_UP:
        #                 cars[0].move(-1, 0)
        #             elif event.key == pygame.K_DOWN:
        #                 cars[0].move(1, 0)
        #             elif event.key == pygame.K_LEFT:
        #                 cars[0].move(0, -1)
        #             elif event.key == pygame.K_RIGHT:
        #                 cars[0].move(0, 1)
        #             print(cars[0].r, cars[0].c, gameMap.game_map[cars[0].r][cars[0].c])
        # Update the display
        pygame.display.flip()
        time.sleep(0.1)

        # else:
        #     # Event handling
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             sys.exit()

        #     keys = pygame.key.get_pressed()
        #     if keys[pygame.K_UP]:
        #         cars[0].move(0, -1)
        #     if keys[pygame.K_DOWN]:
        #         cars[0].move(0, 1)
        #     if keys[pygame.K_LEFT]:
        #         cars[0].move(-1, 0)
        #     if keys[pygame.K_RIGHT]:
        #         cars[0].move(1, 0)

        #     # Update the display
        #     pygame.display.flip()


if __name__ == "__main__":
    main()
