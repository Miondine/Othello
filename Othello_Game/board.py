'''

Class to represent the game board. The positions on the board are saved as a two dimensional list where the first dimension
represents the row of the board and the second dimension the column. Each position is eihter unoccupied (0), white (1) or black (-1).

'''
class Board:

    def __init__(self):
        self.positions = []
        self.NUM_ROWS = 8
        self.NUM_COLS = 8
        self.create_board()

    def create_board(self):

        # initialise board with unoccupied positions
        for row in range(self.NUM_ROWS):
            self.positions.append([])
            for col in range(self.NUM_COLS):
                self.positions[row].append(0)

        # initialise starting postition
        self.positions[3][3] = 1
        self.positions[3][4] = -1
        self.positions[4][3] = -1
        self.positions[4][4] = 1
    
