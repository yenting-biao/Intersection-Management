from parameters import ROWS, COLS, GREEN_WIDTH, ROAD_WIDTH, GREEN, TILE_SIZE, YELLOW
import pygame

# 0 for roads, 1 for non-accessible areas, 2 for horizontal lane lines, 3 for vertical lane lines
class GameMap:
    def __init__(self, screen):
        def generateGameMap() -> list:
            # Initializing an empty map with non-accessible areas (green)
            game_map = [[1 for _ in range(COLS)] for _ in range(ROWS)]
            
            # Calculate center positions
            center_x = COLS // 2
            center_y = ROWS // 2

            # Create the vertical and horizontal roads crossing at the center
            for i in range(ROWS):
                if center_x - ROAD_WIDTH // 2 <= i <= center_x + ROAD_WIDTH // 2:
                    for j in range(COLS):
                        game_map[i][j] = 0
                if center_y - ROAD_WIDTH // 2 <= i <= center_y + ROAD_WIDTH // 2:
                    for j in range(COLS):
                        game_map[j][i] = 0

            # Add lane lines in the center
            mid = ROAD_WIDTH // 2
            for i in range(ROWS):
                for j in range(COLS):
                    if game_map[i][j] == 0:
                        if center_x - ROAD_WIDTH // 2 <= i <= center_x + ROAD_WIDTH // 2 and i % ROAD_WIDTH == mid:
                            game_map[i][j] = 2  # Horizontal lane line
                        if center_y - ROAD_WIDTH // 2 <= j <= center_y + ROAD_WIDTH // 2 and j % ROAD_WIDTH == mid:
                            game_map[i][j] = 3  # Vertical lane line

            return game_map
        
        self.game_map = generateGameMap()
        self.screen = screen
    
    def draw(self):
        # Draw the game map
        for y in range(len(self.game_map)):
            for x in range(len(self.game_map[0])):
                if self.game_map[y][x] == 1:
                    pygame.draw.rect(self.screen, GREEN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                
                if self.game_map[y][x] == 2:
                    DASH_LENGTH = TILE_SIZE // 2
                    DASH_GAP = TILE_SIZE // 2
                    DASH_WIDTH = TILE_SIZE // 8
                    DASH_Y_OFFSET = TILE_SIZE // 2 - DASH_WIDTH // 2
                    for dash_start in range(0, TILE_SIZE, DASH_LENGTH + DASH_GAP):
                        pygame.draw.rect(self.screen, YELLOW, (x * TILE_SIZE + dash_start, y * TILE_SIZE + DASH_Y_OFFSET, DASH_LENGTH, DASH_WIDTH))
                elif self.game_map[y][x] == 3:
                    DASH_LENGTH = TILE_SIZE // 2
                    DASH_GAP = TILE_SIZE // 2
                    DASH_WIDTH = TILE_SIZE // 8
                    DASH_X_OFFSET = TILE_SIZE // 2 - DASH_WIDTH // 2
                    for dash_start in range(0, TILE_SIZE, DASH_LENGTH + DASH_GAP):
                        pygame.draw.rect(self.screen, YELLOW, (x * TILE_SIZE + DASH_X_OFFSET, y * TILE_SIZE + dash_start, DASH_WIDTH, DASH_LENGTH))

# Example parameters
ROWS = 20
COLS = 20
GREEN_WIDTH = 20
ROAD_WIDTH = 2
GREEN = (0, 128, 0)
TILE_SIZE = 20
YELLOW = (255, 255, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((COLS * TILE_SIZE, ROWS * TILE_SIZE))
pygame.display.set_caption("Simple Road Map")

# Create GameMap instance
game_map = GameMap(screen)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Fill the screen with black
    game_map.draw()
    pygame.display.flip()

pygame.quit()
