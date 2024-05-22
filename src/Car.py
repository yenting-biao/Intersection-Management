import pygame
from parameters import RED, TILE_SIZE, COLS, ROWS


# Define the player (car)
class Car:
    def __init__(self, y, x, screen, game_map):
        self.y = y
        self.x = x
        self.screen = screen
        self.game_map = game_map

    def draw(self):
        pygame.draw.circle(
            self.screen,
            RED,
            (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2),
            TILE_SIZE // 2,
        )

    def move(self, dy, dx):
        if (
            0 <= self.x + dx < COLS
            and 0 <= self.y + dy < ROWS
            and self.game_map[self.y + dy][self.x + dx] != 1
        ):
            self.x += dx
            self.y += dy
