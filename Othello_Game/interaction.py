import pygame
import othello_game.constants as c



class Interaction:

    def __init__(self):
        self.window = pygame.display.set_mode((c.WIDTH,c.HEIGHT))

    #draw board and 
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
                    pygame.draw.circle(self.window, c.WHITE, (c.MARGIN + (row + 0.5) * c.SQUARE_SIZE, c.MARGIN + (col + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)   
                elif(board.positions[row][col] == -1):         
                    pygame.draw.circle(self.window, c.BLACK, (c.MARGIN + (row + 0.5) * c.SQUARE_SIZE, c.MARGIN + (col + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)
        

    def draw_possible_moves(self,possible_moves,colour):

        if(colour == 1):
            for move in possible_moves:
                pygame.draw.circle(self.window, c.YELLOW, (c.MARGIN + (move[0] + 0.5) * c.SQUARE_SIZE, c.MARGIN + (move[1] + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)
        if(colour == -1):
            for move in possible_moves:
                pygame.draw.circle(self.window, c.ORANGE, (c.MARGIN + (move[0] + 0.5) * c.SQUARE_SIZE, c.MARGIN + (move[1] + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)

    def draw_selected_position(self,position):

        pygame.draw.circle(self.window, c.DARK_RED, (c.MARGIN + (position[0] + 0.5) * c.SQUARE_SIZE, c.MARGIN + (position[1] + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)