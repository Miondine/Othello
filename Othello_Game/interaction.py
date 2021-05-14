''' 
Interaction objects represents the graphical output and the possibility for a human player to interact with the game
(make move inputs and quit game possibility). All the constants needed tp draw things on the window are determined in
constants. To implement the output and the interaction possibilities, the package pygame is used.
'''

import pygame
import othello_game.constants as c

clock = pygame.time.Clock() # (pygame object) needed for pygame implementations when user input needs to be checked regularly.
FPS = 60 # determines how fast the pygame clock works.

class Interaction:

    
    # initialises object attributes; setup of output/interaction window; sets caption of window to ‘Othello‘. 
    # Changes: self.window.
    def __init__(self):
        self.window = pygame.display.set_mode((c.WIDTH,c.HEIGHT)) # (pygame object) the application window, size is determines by constants WIDTH and HEIGHT.
        pygame.display.set_caption('Othello')

    # draws state of input board on the window.
    # Input: board (Board object). 
    # Changes: self.window.
    def draw_board(self,board):
        self.window.fill(c.BLACK)
        # draw board background
        pygame.draw.rect(self.window,c.GREY,(c.MARGIN,c.MARGIN,c.BOARD_HEIGHT,c.BOARD_WIDTH))
        # draw squares on board
        for row in range(c.NUM_ROWS):
            pygame.draw.line(self.window,c.BLACK,(c.MARGIN, c.MARGIN + row * c.SQUARE_SIZE),(c.MARGIN + c.BOARD_HEIGHT, c.MARGIN + row * c.SQUARE_SIZE),2)
            pygame.draw.line(self.window,c.BLACK,(c.MARGIN + row * c.SQUARE_SIZE, c.MARGIN),(c.MARGIN + row * c.SQUARE_SIZE, c.MARGIN + c.BOARD_WIDTH),2)
            #draw current pieces
            for col in range(c.NUM_COLS):
                if(board.positions[row][col] == 1):
                    pygame.draw.circle(self.window, c.WHITE, (c.MARGIN + (col + 0.5) * c.SQUARE_SIZE, c.MARGIN + (row + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)   
                elif(board.positions[row][col] == -1):         
                    pygame.draw.circle(self.window, c.BLACK, (c.MARGIN + (col + 0.5) * c.SQUARE_SIZE, c.MARGIN + (row + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)
        pygame.display.update()

    # draws all possible positions on the window (only the positions, the board needs to be drawn on the window first). Colour of positions depends
    # on for which player moves are drawn. 
    # Input: possible_positions (2d list, inner lists positions for possibles moves in format [row, col]), colour (1 or -1 depending on player). 
    # Changes: self.window.
    def draw_possible_positions(self,possible_positions,colour):

        if(colour == 1):
            for position in possible_positions:
                pygame.draw.circle(self.window, c.YELLOW, (c.MARGIN + (position[1] + 0.5) * c.SQUARE_SIZE, c.MARGIN + (position[0] + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)
        if(colour == -1):
            for position in possible_positions:
                pygame.draw.circle(self.window, c.ORANGE, (c.MARGIN + (position[1] + 0.5) * c.SQUARE_SIZE, c.MARGIN + (position[0] + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)
        pygame.display.update()
    
    # draws from human player selected position on window.
    # Input: position (list in format [row,col]). 
    # Changes: self.window.
    def draw_selected_position(self,position):

        pygame.draw.circle(self.window, c.DARK_RED, (c.MARGIN + (position[1] + 0.5) * c.SQUARE_SIZE, c.MARGIN + (position[0] + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)
        pygame.display.update()

    # waits for user mouse click, if user clicks exit returns exit code, if user clicks somewhere else function calculates from pixel position 
    # position in [row,col] format. 
    # Output: selected_position (list in format [row,col])
    def get_mouse_position(self):

        while True:
            Interaction.clock.tick(Interaction.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return [100,0]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    row = int((y - c.MARGIN) / c.SQUARE_SIZE)
                    col = int((x - c.MARGIN) / c.SQUARE_SIZE)
                    return [row,col]

