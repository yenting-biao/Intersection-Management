from parameters import ROWS, COLS, GREEN_WIDTH, ROAD_WIDTH, GREEN, TILE_SIZE, WHITE
import pygame

# 0 for roads, 1 for non-accessible areas
# 2 for horizontal lane lines, 3 for vertical lane lines
# 4 for intersection


class GameMap:
    def __init__(self, screen):
        self.screen = screen
        self.game_map = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        for i in range(ROWS):
            for j in range(COLS):
                mid = ROAD_WIDTH // 2
                i_mod = (i + ROAD_WIDTH) % GREEN_WIDTH
                j_mod = (j + ROAD_WIDTH) % GREEN_WIDTH

                if i_mod < ROAD_WIDTH and j_mod < ROAD_WIDTH:
                    self.game_map[i][j] = 4  # Intersection
                elif i_mod == mid:
                    self.game_map[i][j] = 2  # Horizontal lane line
                elif j_mod == mid:
                    self.game_map[i][j] = 3  # Vertical lane line
                elif i_mod < ROAD_WIDTH or j_mod < ROAD_WIDTH:
                    self.game_map[i][j] = 0  # Road
                else:
                    self.game_map[i][j] = 1  # Non-accessible area

    def draw(self):
        # Draw the game map
        for y in range(len(self.game_map)):
            for x in range(len(self.game_map[0])):
                if self.game_map[y][x] == 1:  # Non-accessible area
                    pygame.draw.rect(
                        self.screen,
                        GREEN,
                        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    )

                if self.game_map[y][x] == 2:  # Horizontal lane line
                    DASH_LENGTH = TILE_SIZE // 2
                    DASH_GAP = TILE_SIZE // 2
                    DASH_WIDTH = TILE_SIZE // 8
                    DASH_Y_OFFSET = TILE_SIZE // 2 - DASH_WIDTH // 2
                    for dash_start in range(0, TILE_SIZE, DASH_LENGTH + DASH_GAP):
                        pygame.draw.rect(
                            self.screen,
                            WHITE,
                            (
                                x * TILE_SIZE + dash_start,
                                y * TILE_SIZE + DASH_Y_OFFSET,
                                DASH_LENGTH,
                                DASH_WIDTH,
                            ),
                        )
                elif self.game_map[y][x] == 3:  # Vertical lane line
                    DASH_LENGTH = TILE_SIZE // 2
                    DASH_GAP = TILE_SIZE // 2
                    DASH_WIDTH = TILE_SIZE // 8
                    DASH_X_OFFSET = TILE_SIZE // 2 - DASH_WIDTH // 2
                    for dash_start in range(0, TILE_SIZE, DASH_LENGTH + DASH_GAP):
                        pygame.draw.rect(
                            self.screen,
                            WHITE,
                            (
                                x * TILE_SIZE + DASH_X_OFFSET,
                                y * TILE_SIZE + dash_start,
                                DASH_WIDTH,
                                DASH_LENGTH,
                            ),
                        )
