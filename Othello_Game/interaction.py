import pygame
import othello_game.constants as c


class Interaction:

    def __init__(self):
        self.window = pygame.display.set_mode((c.WIDTH,c.HEIGHT))
        self.FPS = 60
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Othello')

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
                    pygame.draw.circle(self.window, c.WHITE, (c.MARGIN + (col + 0.5) * c.SQUARE_SIZE, c.MARGIN + (row + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)   
                elif(board.positions[row][col] == -1):         
                    pygame.draw.circle(self.window, c.BLACK, (c.MARGIN + (col + 0.5) * c.SQUARE_SIZE, c.MARGIN + (row + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)
        pygame.display.update()

    def draw_possible_positions(self,possible_positions,colour):

        if(colour == 1):
            for position in possible_positions:
                pygame.draw.circle(self.window, c.YELLOW, (c.MARGIN + (position[1] + 0.5) * c.SQUARE_SIZE, c.MARGIN + (position[0] + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)
        if(colour == -1):
            for position in possible_positions:
                pygame.draw.circle(self.window, c.ORANGE, (c.MARGIN + (position[1] + 0.5) * c.SQUARE_SIZE, c.MARGIN + (position[0] + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)
        pygame.display.update()

    def draw_selected_position(self,position):

        pygame.draw.circle(self.window, c.DARK_RED, (c.MARGIN + (position[1] + 0.5) * c.SQUARE_SIZE, c.MARGIN + (position[0] + 0.5) * c.SQUARE_SIZE ), c.RADIUS_DISK)
        pygame.display.update()

    def get_mouse_position(self):

        while True:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return [100,0]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    row = int((y - c.MARGIN) / c.SQUARE_SIZE)
                    col = int((x - c.MARGIN) / c.SQUARE_SIZE)
                    return [row,col]

