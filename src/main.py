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
    LEFT_START,
    LEFT_END,
    TOP_START,
    TOP_END,
    RIGHT_START,
    RIGHT_END,
    BOTTOM_START,
    BOTTOM_END,
    LEFT_COLOR,
    TOP_COLOR,
    RIGHT_COLOR,
    BOTTOM_COLOR,
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


def addCarsRandomly(cars, screen):
    if random.random() < 0.33:
        while True:
            start = random.choice([LEFT_START, TOP_START, RIGHT_START, BOTTOM_START])
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
                        color,
                    )
                )
                break


def solveIntersection(
    controller1: ControlCenter, cars: list[Car], game_map: list[list[int]], drawScreen
):
    result = controller1.schedule()
    print("schedule result", result)

    updateCars = set(result[i][0] for i in range(len(result)))
    for curr in result:
        # Move the cars that are not in the schedule
        for i in range(len(cars)):
            if i in updateCars and not cars[i].justPassedIntersection:
                continue
            dc = controller1.center[1] - cars[i].c
            dr = controller1.center[0] - cars[i].r
            if abs(dc) + abs(dr) > ROAD_WIDTH - 1 or cars[i].justPassedIntersection:
                # will not enter intersection, keep going
                if cars[i].justPassedIntersection:
                    dr = cars[i].destination[0] - cars[i].r
                    dc = cars[i].destination[1] - cars[i].c

                moveDir = (
                    (1 if dr > 0 else -1, 0)
                    if abs(dc) < abs(dr)
                    else (0, 1 if dc > 0 else -1)
                )
                canGo = not any(
                    i != j
                    and cars[i].r + moveDir[0] == cars[j].r
                    and cars[i].c + moveDir[1] == cars[j].c
                    for j in range(len(cars))
                )
                if canGo:
                    if (cars[i].r, cars[i].c) == cars[i].destination:
                        cars[i].color = GRAY
                    else:
                        cars[i].move(moveDir[0], moveDir[1])

        # Move the scheduled cars
        carInd = curr[0]
        dr = curr[1][0] - cars[carInd].r
        dc = curr[1][1] - cars[carInd].c
        cars[carInd].move(dr, dc)

        # Check if the car can leave the intersection
        dr = cars[carInd].destination[0] - cars[carInd].r
        dc = cars[carInd].destination[1] - cars[carInd].c
        tmpDir = (0, 1 if dc > 0 else -1) if dr == 0 else (1 if dr > 0 else -1, 0)
        if game_map[cars[carInd].r + tmpDir[0]][cars[carInd].c + tmpDir[1]] != 4:
            pygame.display.flip()
            time.sleep(SLEEP_TIME)
            drawScreen()
            cars[carInd].justPassedIntersection = True
            cars[carInd].move(tmpDir[0], tmpDir[1])

        pygame.display.flip()
        time.sleep(SLEEP_TIME)
        drawScreen()


def main():
    pygame.init()

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(GRAY)
    pygame.display.set_caption("Intersection Management Simulation")

    # Define the game map
    # 0 for roads, 1 for non-accessible areas,
    # 2 for horizontal lane lines, 3 for vertical lane lines, 4 for intersection
    gameMap = GameMap(screen)
    cars = [
        Car(LEFT_START, TOP_END, screen, LEFT_COLOR),
        Car(RIGHT_START, TOP_END, screen, RIGHT_COLOR),
        Car(TOP_START, BOTTOM_END, screen, TOP_COLOR),
        Car(BOTTOM_START, RIGHT_END, screen, BOTTOM_COLOR),
    ]

    def drawScreen():
        screen.fill(GRAY)

        gameMap.draw()

        # Draw the player car
        for car in cars:
            car.draw()

    # Main loop
    while len(cars) > 0:
        drawScreen()

        # update the car positions normally
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

        # schedule the cars to pass the intersection
        if len(controller1.carList) > 0:
            solveIntersection(controller1, cars, gameMap.game_map, drawScreen)

        # Remove cars that have reached their destination
        cars = [car for car in cars if not (car.r, car.c) == car.destination]

        # Randomly add new cars
        addCarsRandomly(cars, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    random.seed(0)
    main()
