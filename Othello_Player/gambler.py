import othello_player.player as player
import random

'''
This class represents the AI Roxanne. This class is derived from Player class. Roxanne plays
after a value table. The value table contains for each position on the board a value reflecting
how good the position is. If itis her move she looks up the values for all possible moves and
then randomly picks on of the positions with the best value. 
'''

class Gambler(player.Player):

    # calls __init__(colour) to initialise player attributes.
    # Input: colour (int)
    def __init__(self, colour):
        super().__init__(colour)
    
    # calls get_possible_positions(board). If no positions available returns made_move = False and input board
    # state, else picks one board state randomly from possible_moves and returns it. 
    # Input: board (Board objects).
    # Output: made_move (True if player made a move, False if passed), board (new board state, or input if player passed
    def make_move(self, board):

        self.get_possible_moves(board)

        # no move possible
        if(self.possible_positions == []):
            made_move = False
            return made_move, board
        else: 
            made_move = True

        #return radom board state from possible_moves
        return made_move, random.choice(self.possible_moves)
        
    #calls get_possible_positions(board). If no positions available returns made_move = False and input board
    # state, else picks one board state randomly from possible_moves and returns it.
    # Input: board (Board objects). 
    # Output: quit_val (always False), made_move (True if player made a move, False if passed), 
    # board (new board state, or input if player passed)
    def make_move_graphical(self, board):

        quit_val = False
        self.get_possible_moves(board)

        # no move possible
        if(self.possible_positions == []):
            made_move = False
            return made_move, board
        else: 
            made_move = True

        #return radom board state from possible_moves
        return quit_val, made_move, random.choice(self.possible_moves)
        