# constants for board setup
NUM_COLS = 8
NUM_ROWS = 8
NUM_DIAGONALS = 13

# constants for graphical interface
HEIGHT = 800
MARGIN_TOP = int(HEIGHT * 0.125)
MARGIN_BOTTOM = int(HEIGHT * 0.05)
BOARD_SIZE = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
MARGIN_SIDE = int(BOARD_SIZE * 0.25)
WIDTH = BOARD_SIZE + 2 * MARGIN_SIDE
SQUARE_SIZE = int(BOARD_SIZE / NUM_COLS)
RADIUS_DISK = (0.5 * SQUARE_SIZE) * 0.8
NEXT_BUTTON_WIDTH = int(MARGIN_SIDE * 0.75)
NEXT_BUTTON_HEIGHT = int(NEXT_BUTTON_WIDTH * 0.55)
NEXT_BUTTON_FONTSIZE = int(NEXT_BUTTON_HEIGHT * 0.8)
NEXT_BUTTON_x = BOARD_SIZE + MARGIN_SIDE + int(0.5 * (MARGIN_SIDE - NEXT_BUTTON_WIDTH))
NEXT_BUTTON_y = MARGIN_TOP + 0.5 * SQUARE_SIZE
INFO_FONT_SIZE = int(MARGIN_TOP * 0.3)
#colours:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128,128,128)
DARK_GREY = (100,100,100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_RED = (153,0,0)
YELLOW = (255,255,0)
ORANGE = (255,128,0)