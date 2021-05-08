'''

Class to represent the game board. The positions on the board are saved as a two dimensional list where the first dimension
represents the row of the board and the second dimension the column. Each position is eihter unoccupied (0), white (1) or black (-1).

'''
import othello_game.constants as c

class Board:

    def __init__(self):
        self.positions = []
        
        self.create_board()

    def create_board(self):

        # initialise board with unoccupied positions
        for row in range(c.NUM_ROWS):
            self.positions.append([])
            for col in range(c.NUM_COLS):
                self.positions[row].append(0)

        # initialise starting postition
        self.positions[3][3] = 1
        self.positions[3][4] = -1
        self.positions[4][3] = -1
        self.positions[4][4] = 1
    
