'''
Board object is for the representation of the game board. It contains the current state of the game.
'''
import othello_game.constants as c

class Board:

    # initializes object attributes, all of them are determined by the rules of the game, calls function create_board().
    # Changes: self. positions, self.discs_black/white, self.num_positions, self.empty_positions, self_num_rows/cols.
    def __init__(self):
        # (2d List) containing the actual game board representation. 
        # Each inner list contains one row of the board. Each element is either 0 (empty), 1 (black) or -1 (white).
        self.positions = [] 

        self.discs_black = 2
        self.discs_white = 2
        self.num_positions = (c.NUM_ROWS * c.NUM_ROWS)
        self.empty_positions = self.num_positions - 4
        self.num_rows = c.NUM_ROWS
        self.num_cols = c.NUM_COLS

        # call func to initialise positions 
        self.create_board()

    # initialises the board positions according to the rules.  
    # Changes: self.positions
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
    
    # calculates current number of discs in each colour and the empty positions. 
    # Changes: self.discs_black/white, self.empty_positions.
    def update_num_discs(self):
        temp_discs_black = 0
        temp_discs_white = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if (self.positions[row][col] == -1):
                    temp_discs_white += 1
                elif (self.positions[row][col] == 1):
                    temp_discs_black += 1
        
        self.discs_black = temp_discs_black
        self.discs_white = temp_discs_white
        self.empty_positions = self.num_positions - self.discs_white - self.discs_black

    



