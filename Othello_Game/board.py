'''

Class to represent the game board. The positions on the board are saved as a two dimensional list where the first dimension
represents the row of the board and the second dimension the column. Each position is eihter unoccupied (0), white (1) or black (-1).

'''
import othello_game.constants as c

class Board:

    def __init__(self):
        self.positions = []
        self.disks_black = 2
        self.disks_white = 2
        self.num_positions = (c.NUM_ROWS * c.NUM_ROWS)
        self.empty_positions = self.num_positions - 4
        self.num_rows = c.NUM_ROWS
        self.num_cols = c.NUM_COLS
        self.create_board()

    def create_board(self):

        # initialise board with unoccupied positions
        for row in range(self.num_rows):
            self.positions.append([])
            for col in range(self.num_cols):
                self.positions[row].append(0)

        # initialise starting postition
        self.positions[3][3] = 1
        self.positions[3][4] = -1
        self.positions[4][3] = -1
        self.positions[4][4] = 1
    
    def update_num_diks(self):
        temp_disks_black = 0
        temp_disks_white = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if (self.positions[row][col] == 1):
                    temp_disks_white += 1
                elif (self.positions[row][col] == -1):
                    temp_disks_black += 1
        
        self.disks_black = temp_disks_black
        self.disks_white = temp_disks_white
        self.empty_positions = self.num_positions - self.disks_white - self.disks_black

    



