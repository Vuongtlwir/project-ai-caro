BOARD_SIZE = 15
WIN_LENGTH = 5

EMPTY = 0
HUMAN = 1
AI = -1

DRAW = 2

INF = 10**18

MAX_DEPTH = 4

CELL_SIZE = 40

WIDTH = BOARD_SIZE * CELL_SIZE
HEIGHT = BOARD_SIZE * CELL_SIZE

FPS = 60

# directions: horizontal, vertical, diagonals
DIRECTIONS = [
    (0, 1),     # horizontal
    (1, 0),     # vertical
    (1, 1),     # diagonal down-right
    (1, -1)     # diagonal down-left
]