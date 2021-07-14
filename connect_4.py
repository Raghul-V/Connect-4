import pygame
import sys


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BG_COLOR = BLACK
BOARD_COLOR = BLUE

PLAYER1 = RED
PLAYER2 = YELLOW

ROWS = 6
COLS = 7

BOX_WIDTH = 75

SCREEN_WIDTH = BOX_WIDTH * COLS
SCREEN_HEIGHT = BOX_WIDTH * (ROWS + 2)

BOARD_Y = BOX_WIDTH * 2

SIDE_SPACE = BOX_WIDTH / 10
DIAMETER = BOX_WIDTH - (2 * SIDE_SPACE)
RADIUS = DIAMETER / 2

position = [[0 for j in range(COLS)] for i in range(ROWS)]
colors = { 0: BG_COLOR, 1: PLAYER1, 2: PLAYER2 }


class Disc:
    def __init__(self, color):
        self.color = color
        self.x = 0
        self.y = 0

    def move(self):
        x, y = pygame.mouse.get_pos()
        
        if x < RADIUS:
            x = RADIUS
        elif x > SCREEN_WIDTH - RADIUS:
            x = SCREEN_WIDTH - RADIUS
        
        if y < RADIUS:
            y = RADIUS
        elif y > BOARD_Y - RADIUS:
            y = BOARD_Y - RADIUS
        
        self.x = x
        self.y = y

    def display(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), RADIUS)


def draw_window(surface):
    # Background
    surface.fill(BG_COLOR)

    # Board
    pygame.draw.rect(surface, BOARD_COLOR, (0, BOARD_Y, SCREEN_WIDTH, SCREEN_HEIGHT-BOARD_Y))
    for i in range(ROWS):
        for j in range(COLS):
            x = RADIUS + SIDE_SPACE + (BOX_WIDTH)*j
            y = BOARD_Y + RADIUS + SIDE_SPACE + (BOX_WIDTH)*i
            color = colors[position[i][j]]
            pygame.draw.circle(surface, color, (x, y), RADIUS)

def has_won(player):
    for i in range(ROWS):
        for j in range(COLS):
            # Horizontal line
            if j < COLS-3:
                if position[i][j] == position[i][j+1] == position[i][j+2] == position[i][j+3] == player:
                    return True
            # Vertical line
            if i < ROWS-3:
                if position[i][j] == position[i+1][j] == position[i+2][j] == position[i+3][j] == player:
                    return True
            # Top-to-bottom Diagonal line
            if i < ROWS-3 and j < COLS-3:
                if position[i][j] == position[i+1][j+1] == position[i+2][j+2] == position[i+3][j+3] == player:
                    return True
            # Bottom-to-top Diagonal line
            if i > 2 and j < COLS-3:
                if position[i][j] == position[i-1][j+1] == position[i-2][j+2] == position[i-3][j+3] == player:
                    return True
    return False

def is_board_filled():
    for i in range(ROWS):
        if 0 in position[i]:
            return False
    return True

def display_game_result(surface, result, font):
    text = font.render(result, True, WHITE)
    x = (SCREEN_WIDTH - text.get_width()) / 2
    y = (BOARD_Y - text.get_height()) / 2
    surface.blit(text, (x, y))


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect 4")
pygame.display.set_icon(pygame.image.load("icon.png"))

font = pygame.font.SysFont("monospace", BOARD_Y//4)

disc = Disc(PLAYER1)
game_result = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_result:
                continue
            for i in range(ROWS-1, -1, -1):
                j = int(disc.x / BOX_WIDTH)
                if position[i][j] != 0:
                    continue
                if disc.color == PLAYER1:
                    position[i][j] = 1
                    disc.color = PLAYER2
                else:
                    position[i][j] = 2
                    disc.color = PLAYER1
                break

    draw_window(screen)

    if not game_result:
        disc.move()
        disc.display(screen)
        
        if has_won(1):
            game_result = "Player 1 won the game!"
        elif has_won(2):
            game_result = "Player 2 won the game!"
        elif is_board_filled():
            game_result = "Match Tie!"
    else:
        display_game_result(screen, game_result, font)
    
    pygame.display.update()


