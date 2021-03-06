import othello_player.player as player
import random

'''
This Class represents a player, who plays such that he flips with every move the maximum amount of discs. 
This class is derived from Player class. If more two or more moves would flip the maximum amount of discs,
the greedy player choses one randomly.
'''
class Greedy(player.Player):

    # calls __init__(colour) to initialise player attributes.
    # Input: colour (int)
    def __init__(self, colour, graphical, graphical_interface):
        super().__init__(colour, graphical ,graphical_interface)
    
    # calls get_possible_positions(board). If no positions available returns made_move = False and input board state,
    # else calculates for each move how many discs would be flipped.  Returns one of the moves, where the most discs 
    # get flipped randomly chosen. 
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

        # save number of own diks in current board state
        if(self.colour == 1):
            num_own_discs = board.discs_black
        else:
            num_own_discs = board.discs_white

        # make list of how much discs get flipped at each position (list is in same order as possible_positions)
        disc_differences = []
        for move in self.possible_moves:

            if(self.colour == 1):
                disc_difference = move.discs_black - num_own_discs
            else:
                disc_difference = move.discs_white - num_own_discs

            disc_differences.append(disc_difference)

        # find indices of positions where most discs get flipped
        max_value = max(disc_differences)
        indices_best_positions = [index for index, value in enumerate(disc_differences) if value == max_value]

        #return board state which corresponds to random choice of positions where most discs are flipped
        return made_move, self.possible_moves[random.choice(indices_best_positions)]
        
    # calls get_possible_positions(board). If no positions available returns made_move = False and input board state,
    # else calculates for each move how many discs would be flipped.  Returns one of the moves, where the most discs 
    # get flipped randomly chosen. 
    # Input: board (Board objects). 
    # Output: quit_val (always False), made_move (True if player made a move, False if passed), 
    # board (new board state, or input if player passed)
    def make_move_graphical(self, board):

        quit_val = False
        self.get_possible_moves(board)

        # no move possible
        if(self.possible_positions == []):
            made_move = False
            return quit_val, made_move, board
        else: 
            made_move = True

        # save number of own diks in current board state
        if(self.colour == 1):
            num_own_discs = board.discs_black
        else:
            num_own_discs = board.discs_white

        # make list of how much discs get flipped at each position (list is in same order as possible_positions)
        disc_differences = []
        for move in self.possible_moves:

            if(self.colour == 1):
                disc_difference = move.discs_black - num_own_discs
            else:
                disc_difference = move.discs_white - num_own_discs

            disc_differences.append(disc_difference)

        # find indices of positions where most discs get flipped
        max_value = max(disc_differences)
        indices_best_positions = [index for index, value in enumerate(disc_differences) if value == max_value]

        #return board state which corresponds to random choice of positions where most discs are flipped
        return quit_val, made_move, self.possible_moves[random.choice(indices_best_positions)]
        