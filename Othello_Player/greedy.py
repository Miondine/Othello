import othello_player.player as player
import random


class Greedy(player.Player):

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

        # save number of own diks in current board state
        if(self.colour == 1):
            num_own_disks = board.disks_white
        else:
            num_own_disks = board.disks_black

        # make list of how much disks get flipped at each position (list is in same order as possible_positions)
        disk_differences = []
        for move in self.possible_moves:

            if(self.colour == 1):
                disk_difference = move.disks_white - num_own_disks
            else:
                disk_difference = move.disks_black - num_own_disks

            disk_differences.append(disk_difference)

        # find indices of positions where most disks get flipped
        max_value = max(disk_differences)
        indices_best_positions = [index for index, value in enumerate(disk_differences) if value == max_value]

        #return board state which corresponds to random choice of positions where most disks are flipped
        return made_move, self.possible_moves[random.choice(indices_best_positions)]
        

        
    # calls get_possible_positions(board). If no positions available returns made_move = False and input board
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
            return quit_val, made_move, board
        else: 
            made_move = True

        # save number of own diks in current board state
        if(self.colour == 1):
            num_own_disks = board.disks_white
        else:
            num_own_disks = board.disks_black

        # make list of how much disks get flipped at each position (list is in same order as possible_positions)
        disk_differences = []
        for move in self.possible_moves:

            if(self.colour == 1):
                disk_difference = move.disks_white - num_own_disks
            else:
                disk_difference = move.disks_black - num_own_disks

            disk_differences.append(disk_difference)

        # find indices of positions where most disks get flipped
        max_value = max(disk_differences)
        indices_best_positions = [index for index, value in enumerate(disk_differences) if value == max_value]

        #return board state which corresponds to random choice of positions where most disks are flipped
        return quit_val, made_move, self.possible_moves[random.choice(indices_best_positions)]
        