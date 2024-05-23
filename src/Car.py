import pygame
from parameters import RED, TILE_SIZE, COLS, ROWS


# Define the player (car)
class Car:
    def __init__(
        self,
        source: tuple[int, int],
        destination: tuple[int, int],
        screen,
        game_map,
        color=RED,
    ):
        self.r = source[0]
        self.c = source[1]
        self.source = source
        self.destination = destination
        self.screen = screen
        self.game_map = game_map
        self.color = color

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.c * TILE_SIZE + TILE_SIZE // 2, self.r * TILE_SIZE + TILE_SIZE // 2),
            TILE_SIZE // 2,
        )

    def move(self, dr, dc):
        if (
            0 <= self.c + dc < COLS
            and 0 <= self.r + dr < ROWS
            and self.game_map[self.r + dr][self.c + dc] != 1
        ):
            self.c += dc
            self.r += dr
