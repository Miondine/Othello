import othello_player.player as player
import random

'''
This class represents the AI Roxanne. This class is derived from Player class. Roxanne plays
after a value table. The value table contains for each position on the board a value reflecting
how good the position is. If itis her move she looks up the values for all possible moves and
then randomly picks on of the positions with the best value. 
'''

class Roxanne(player.Player):

    # (2d list) each inner list represents one row of the game board. The entries of the 
    # inner list are the values of the position. Values are ints from 1 to 5, where 1 have
    # the best positions and 5 the worst ones.
    board_values = [[1,5,3,3,3,3,5,1],
                    [5,5,4,4,4,4,5,5],
                    [3,4,2,2,2,2,4,3],
                    [3,4,2,0,0,2,4,3],
                    [3,4,2,0,0,2,4,3],
                    [3,4,2,2,2,2,4,3],
                    [5,5,4,4,4,4,5,5],
                    [1,5,3,3,3,3,5,1]]

    # calls __init__(colour) to initialise player attributes.
    # Input: colour (int)
    def __init__(self, colour):
        super().__init__(colour)
    
    # calls get_possible_positions(board). If no positions available returns made_move = False
    # and input board state, else calculates values of all possible positions and returns one 
    # of the positions with the best value randomly chosen.
    # Input: board (Board objects). 
    # Output: made_move (True if player made a move, False if passed), board (new board state,
    # or input if player passed)
    def make_move(self, board):

        made_move = True
        player.get_possible_move(board)

        # no move possible
        if(self.possible_positions == []):
            made_move = False
            return made_move, board
        
        # calculate board value for all possible_positions:
        position_values = []
        for position in self.possible_positions:
            position_values.append(Roxanne.board_values[position[0]][position[1]])

        # find indices of positions with best values:
        min_value = min(position_values)
        indices_best_positions = [index for index, value in position_values if value == min_value]

        #return board state which corresponds to random choice of positions with best values
        return made_move, self.possible_moves[random.choice(indices_best_positions)]

