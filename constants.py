# Shared constants (like ROWS, COLS, COLORS, moves, start/goal)

ROWS, COLS = 5, 6
CELL_SIZE = 80
BUTTON_HEIGHT = 35
BUTTON_GAP = 20
NUM_BUTTON_ROWS = 1
WINDOW_HEIGHT = ROWS * CELL_SIZE + NUM_BUTTON_ROWS * BUTTON_HEIGHT

start = (0, 0)
goal = (4, 5)

moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

DEFAULT_OBSTACLES = {(0, 1), (2, 1), (3, 1), (2, 3), (3, 4), (4, 4)}
NUM_OBSTACLES = 8
