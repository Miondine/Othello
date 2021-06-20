import othello_player.player as player
from copy import deepcopy

class StaticBoard(heuristics.Heuristic):

    static_board = [[4,-3,2,2,2,2,-3,4],
                    [-3,-4,-1,-1,-1,-1,-4,-3],
                    [2,-1,1,0,0,1,-1,2],
                    [2,-1,0,1,1,0,-1,2],
                    [2,-1,0,1,1,0,-1,2],
                    [2,-1,1,0,0,1,-1,2],
                    [-3,-4,-1,-1,-1,-1,-4,-3],
                    [4,-3,2,2,2,2,-3,4]]

    def __init__(self, colour, graphical, graphical_interface):
        super().__init__(colour, graphical ,graphical_interface)
        self.max_depth = 4
        self.max_heuristic_val = 200
        self.min_heuristic_val = -200

    def make_move(self,board):

        max_player = player.Player(self.colour, False, None)
        min_player = player.Player(self.opponent_colour, False, None)

        self.get_possible_moves(board)
        if(self.possible_moves == []):
            return False, board
        else:
            alpha = self.min_heuristic_val
            beta = self.max_heuristic_val
            value = alpha
            for move in self.possible_moves:
                possible_value = - self.get_alpha_beta_value(move, min_player, max_player, 1, True, -beta, -value)
                if(possible_value > value):
                    value = possible_value
                    current_best_move = move
                if(value >= beta):
                    break

            return True, current_best_move

    def make_move_graphical(self,board):

        quit_val = False
        self.update_heuristic_values

        max_player = player.Player(self.colour, True, self.graphical_interface)
        min_player = player.Player(self.opponent_colour, True, self.graphical_interface)

        self.get_possible_moves(board)

        # draw possible positions
        self.graphical_interface.draw_possible_positions(self.possible_positions, self.colour)
        
        if(self.possible_moves == []):
            return quit_val, False, [0,0],board
        else:
            alpha = self.min_heuristic_val
            beta = self.max_heuristic_val
            value = alpha
            for move, index in enumerate(self.possible_moves):
                possible_value = - self.get_alpha_beta_value(move, min_player, max_player, 1, True, -beta, -value)
                if(possible_value > value):
                    value = possible_value
                    move_index = index
                if(value >= beta):
                    break

            return quit_val, True, self.possible_positions[move_index], self.possible_moves[move_index]


    def get_alpha_beta_value(self,board, playing_player, waiting_player,depth, moved, alpha, beta):
        # board full, game ends
        if(board.empty_positions == 0):
            if (playing_player.colour == 1):
                coin_difference = board.diks_white - board.disks_black
            else:
                coin_difference = board.disks_black - board.disks_white
            if (coin_difference > 0):
                value = coin_difference + 100
            else:
                value = coin_difference - 100
        elif(depth == self.max_depth):
            playing_player_value, waiting_player_value = self.get_static_board_value(board, playing_player.colour, waiting_player.colour)
            value = playing_player_value - waiting_player_value
        else:
            value = alpha
            playing_player.get_possible_moves(board)
            if (playing_player.possible_moves == []):
                # game ends if both players can't move
                if (moved == False):
                    if (playing_player.colour == 1):
                        coin_difference = board.diks_white - board.disks_black
                    else:
                        coin_difference = board.disks_black - board.disks_white
                    if (coin_difference > 0):
                        value = coin_difference + 100
                    else:
                        value = coin_difference - 100
                # no moves possible next players turn
                else:
                    value = - self.get_alpha_beta_value(board, waiting_player, playing_player, depth+1, False, -beta, -value)
            else:
                # go one step further in the tree for all possible moves
                for move in playing_player.possible_moves:
                    possible_value = - self.get_alpha_beta_value(move, waiting_player, playing_player, depth+1, True, -beta, -value)
                    if(possible_value > value):
                        value = possible_value
                    if(value >= beta):
                        break
                    
        return value            

    def get_static_board_values(self,board, colour, opponent_colour):
        
        own_value = 0
        opponent_value = 0
        for row in range(board.num_rows):
            for col in range(board.num_cols):
                if(board.positions[row][col] == colour):
                    own_value += StaticBoard.static_board[row][col]
                elif(board.positions[row][col] == opponent_colour):
                    opponent_value += StaticBoard.static_board[row][col]

        return own_value, opponent_value
