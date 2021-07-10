from numpy.core.fromnumeric import choose
import othello_player.player as player
import random

'''
This class represents the AI Roxanne. This class is derived from Player class. Roxanne plays
after a value table. The value table contains for each position on the board a value reflecting
how good the position is. If itis her move she looks up the values for all possible moves and
then randomly picks on of the positions with the best value. 
'''

class RoxanneDynamic(player.Player):

    # calls __init__(colour) to initialise player attributes.
    # Input: colour (int)
    def __init__(self, colour, graphical, graphical_interface):
        super().__init__(colour, graphical ,graphical_interface)
        # (2d list) each inner list represents one row of the game board. The entries of the 
        # inner list are the values of the position. Values are ints from 1 to 5, where 1 have
        # the best positions and 5 the worst ones.
        self.board_values = [[1,5,3,3,3,3,5,1],
                        [5,5,4,4,4,4,5,5],
                        [3,4,2,2,2,2,4,3],
                        [3,4,2,0,0,2,4,3],
                        [3,4,2,0,0,2,4,3],
                        [3,4,2,2,2,2,4,3],
                        [5,5,4,4,4,4,5,5],
                        [1,5,3,3,3,3,5,1]]
    
    # calls get_possible_positions(board). If no positions available returns made_move = False
    # and input board state, else calculates values of all possible positions and returns one 
    # of the positions with the best value randomly chosen.
    # Input: board (Board objects). 
    # Output: made_move (True if player made a move, False if passed), board (new board state,
    # or input if player passed)
    def make_move(self, board):

        made_move = True
        self.get_possible_moves(board)

        # no move possible
        if(self.possible_positions == []):
            made_move = False
            return made_move, board
        
        # calculate board value for all possible_positions:
        position_values = []
        for position in self.possible_positions:
            position_values.append(self.board_values[position[0]][position[1]])

        # find indices of positions with best values:
        min_value = min(position_values)
        indices_best_positions = [index for index, value in enumerate(position_values) if value == min_value]
        chosen_index = random.choice(indices_best_positions)
        position = self.possible_positions[chosen_index]
        # if Roxanne occupies corner position update board values of adjacent positions 
        if(position == [0,0]):
            self.board_values[0][1] = 3
            self.board_values[1][0] = 3
            self.board_values[1][1] = 3
        elif(position == [0,7]):
            self.board_values[1][7] = 3
            self.board_values[0][6] = 3
            self.board_values[1][6] = 3
        elif(position == [7,0]):
            self.board_values[7][1] = 3
            self.board_values[6][0] = 3
            self.board_values[6][1] = 3
        elif(position == [7,7]):
            self.board_values[7][6] = 3
            self.board_values[7][6] = 3
            self.board_values[6][6] = 3

        #return board state which corresponds to random choice of positions with best values
        return made_move, self.possible_moves[chosen_index]
        
    # calls get_possible_positions(board). If no positions available returns made_move = False and input board
    # state, else calculates values of all possible positions and returns one of the positions with the best 
    # value randomly chosen. 
    # Input: board (Board objects). 
    # Output: quit_val (always False), made_move (True if player made a move, False if passed), 
    # board (new board state, or input if player passed)
    def make_move_graphical(self, board):

        made_move = True
        quit_val = False
        self.get_possible_moves(board)

        # no move possible
        if(self.possible_positions == []):
            made_move = False
            return quit_val, made_move, [0,0],board
        
        # calculate board value for all possible_positions:
        position_values = []
        for position in self.possible_positions:
            position_values.append(self.board_values[position[0]][position[1]])

        # find indices of positions with best values:
        min_value = min(position_values)
        indices_best_positions = [index for index, value in enumerate(position_values)  if value == min_value]
        chosen_index = random.choice(indices_best_positions)
        position = self.possible_positions[chosen_index]
        # if Roxanne occupies corner position update board values of adjacent positions 
        if(position == [0,0]):
            self.board_values[0][1] = 3
            self.board_values[1][0] = 3
            self.board_values[1][1] = 3
        elif(position == [0,7]):
            self.board_values[1][7] = 3
            self.board_values[0][6] = 3
            self.board_values[1][6] = 3
        elif(position == [7,0]):
            self.board_values[7][1] = 3
            self.board_values[6][0] = 3
            self.board_values[6][1] = 3
        elif(position == [7,7]):
            self.board_values[7][6] = 3
            self.board_values[7][6] = 3
            self.board_values[6][6] = 3
        #return board state which corresponds to random choice of positions with best values
        return quit_val, made_move, self.possible_positions[chosen_index],self.possible_moves[chosen_index]

