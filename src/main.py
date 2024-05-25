import pygame
import sys
import time
import random
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
    SLEEP_TIME,
)
from Car import Car

random.seed(0)


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
        Car(LEFT_START, TOP_END, screen, gameMap.game_map, LEFT_COLOR),
        Car(RIGHT_START, LEFT_END, screen, gameMap.game_map, RIGHT_COLOR),
        Car(TOP_START, BOTTOM_END, screen, gameMap.game_map, TOP_COLOR),
        Car(BOTTOM_START, RIGHT_END, screen, gameMap.game_map, BOTTOM_COLOR),
    ]

    def drawScreen():
        screen.fill(GRAY)

        gameMap.draw()

        # Draw the player car
        for car in cars:
            car.draw()

    # Main game loop
    while True:
        drawScreen()

        controller1 = ControlCenter((27, 27))
        for i in range(len(cars)):
            dc = controller1.center[1] - cars[i].c
            dr = controller1.center[0] - cars[i].r
            if (
                abs(dc) + abs(dr) > ROAD_WIDTH - 1
                and not cars[i].justPassedIntersection
            ):  # int(ROAD_WIDTH * 2):
                # far from intersection, keep going
                if abs(dc) < abs(dr):  # move vertically
                    cars[i].move(1 if dr > 0 else -1, 0)
                else:  # move horizontally
                    cars[i].move(0, 1 if dc > 0 else -1)
            elif cars[i].justPassedIntersection:
                dr = cars[i].destination[0] - cars[i].r
                dc = cars[i].destination[1] - cars[i].c
                if dr == 0 and dc == 0:
                    continue
                elif dr == 0:
                    cars[i].move(0, 1 if dc > 0 else -1)
                else:
                    cars[i].move(1 if dr > 0 else -1, 0)
            else:
                # near intersection, need to call control center
                trajectory = generateTrajectory(cars[i], controller1, gameMap.game_map)
                # print("trajectory", trajectory)
                controller1.addCar({"index": i, "trajectory": trajectory})

        if len(controller1.carList) > 0:
            # schedule the cars
            result = controller1.schedule()
            print("schedule result", result)

            updateCars = set(result[i][0] for i in range(len(result)))
            for curr in result:
                pygame.display.flip()
                time.sleep(SLEEP_TIME)
                drawScreen()

                carInd = curr[0]
                dr = curr[1][0] - cars[carInd].r
                dc = curr[1][1] - cars[carInd].c
                cars[carInd].move(dr, dc)

                # TODO: bug here, need to fix
                for i in range(len(cars)):
                    if i in updateCars:
                        continue
                    dc = controller1.center[1] - cars[i].c
                    dr = controller1.center[0] - cars[i].r
                    if (
                        abs(dc) + abs(dr) > ROAD_WIDTH - 1
                        and not cars[i].justPassedIntersection
                    ):  # int(ROAD_WIDTH * 2):
                        # far from intersection, keep going
                        canGo = True
                        moveDir = (
                            (1 if dr > 0 else -1, 0)
                            if abs(dc) < abs(dr)
                            else (0, 1 if dc > 0 else -1)
                        )

                        for j in range(len(cars)):
                            if (
                                i != j
                                and cars[i].r + moveDir[0] == cars[j].r
                                and cars[i].c + moveDir[1] == cars[j].c
                            ):
                                canGo = False
                                break
                        if canGo:
                            cars[i].move(moveDir[0], moveDir[1])

                    elif cars[i].justPassedIntersection:
                        dr = cars[i].destination[0] - cars[i].r
                        dc = cars[i].destination[1] - cars[i].c

                        canGo = True
                        moveDir = (
                            (1 if dr > 0 else -1, 0)
                            if abs(dc) < abs(dr)
                            else (0, 1 if dc > 0 else -1)
                        )

                        for j in range(len(cars)):
                            if (
                                i != j
                                and cars[i].r + moveDir[0] == cars[j].r
                                and cars[i].c + moveDir[1] == cars[j].c
                            ):
                                canGo = False
                                break
                        if canGo:
                            if dr == 0 and dc == 0:
                                continue
                            elif dr == 0:
                                cars[i].move(0, 1 if dc > 0 else -1)
                            else:
                                cars[i].move(1 if dr > 0 else -1, 0)

            for carInd in updateCars:
                dr = cars[carInd].destination[0] - cars[carInd].r
                dc = cars[carInd].destination[1] - cars[carInd].c
                cars[carInd].justPassedIntersection = True
                if dr == 0:
                    cars[carInd].move(0, 1 if dc > 0 else -1)
                else:
                    cars[carInd].move(1 if dr > 0 else -1, 0)

                pygame.display.flip()
                time.sleep(SLEEP_TIME)

                drawScreen()

        # Remove cars that have reached their destination
        cars = [car for car in cars if not (car.r, car.c) == car.destination]

        # Randomly add new cars
        if random.random() < 0.3:
            while True:
                start = random.choice(
                    [LEFT_START, TOP_START, RIGHT_START, BOTTOM_START]
                )
                end = random.choice([LEFT_END, TOP_END, RIGHT_END, BOTTOM_END])
                if abs(start[0] - end[0]) + abs(start[1] - end[1]) > ROAD_WIDTH:
                    color = (
                        TOP_COLOR
                        if start == TOP_START
                        else (
                            BOTTOM_COLOR
                            if start == BOTTOM_START
                            else (LEFT_COLOR if start == LEFT_START else RIGHT_COLOR)
                        )
                    )
                    cars.append(
                        Car(
                            start,
                            end,
                            screen,
                            gameMap.game_map,
                            color,
                        )
                    )
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
