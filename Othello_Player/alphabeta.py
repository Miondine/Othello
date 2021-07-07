import othello_player.heuritics as heuristics
from copy import deepcopy

class AlphaBeta(heuristics.Heuristic):

    def __init__(self, colour, graphical, graphical_interface):
        super().__init__(colour, graphical ,graphical_interface)
        self.max_depth = 7
        self.max_heuristic_val = 100
        self.min_heuristic_val = -100

    def make_move(self,board):

        self.update_heuristic_values

        max_player = heuristics.Heuristic(self.colour, False, None)
        min_player = heuristics.Heuristic(self.opponent_colour, False, None)

        self.get_possible_moves(board)
        if(self.possible_moves == []):
            return False, board
        else:
            alpha = self.min_heuristic_val - 128
            beta = self.max_heuristic_val + 128
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

        max_player = heuristics.Heuristic(self.colour, True, self.graphical_interface)
        min_player = heuristics.Heuristic(self.opponent_colour, True, self.graphical_interface)

        self.get_possible_moves(board)

        # draw possible positions
        self.graphical_interface.draw_possible_positions(self.possible_positions, self.colour)
        
        if(self.possible_moves == []):
            return quit_val, False, [0,0],board
        else:
            alpha = self.min_heuristic_val - 128
            beta = self.max_heuristic_val + 128
            value = alpha
            for index, move in enumerate(self.possible_moves):
                possible_value = - self.get_alpha_beta_value(move, min_player, max_player, 1, True, -beta, -value)
                if(possible_value > value):
                    value = possible_value
                    move_index = index
                if(value >= beta):
                    break

            return quit_val, True, self.possible_positions[move_index], self.possible_moves[move_index]


    def reset_stability(self, playing_player):

        playing_player.full_cols = deepcopy(self.full_cols)
        playing_player.full_rows = deepcopy(self.full_rows)
        playing_player.full_left_diagonals = deepcopy(self.full_left_diagonals)
        playing_player.full_right_diagonals = deepcopy(self.full_right_diagonals)
        if(playing_player.colour == self.colour):
            playing_player.stability_board = deepcopy(self.stability_board)
            playing_player.opponent_stability_board = deepcopy(self.opponent_stability_board)
        else:
            playing_player.stability_board = deepcopy(self.opponent_stability_board)
            playing_player.opponent_stability_board = deepcopy(self.stability_board)


    def get_alpha_beta_value(self,board, playing_player, waiting_player,depth, moved, alpha, beta):
        # board full, game ends
        if(board.empty_positions == 0):
            if (playing_player.colour == 1):
                coin_difference = board.discs_black - board.discs_white
            else:
                coin_difference = board.discs_white - board.discs_black
            if (coin_difference > 0):
                value = coin_difference + self.max_heuristic_val
            else:
                value = coin_difference + self.min_heuristic_val
        elif(depth == self.max_depth):
            self.reset_stability(playing_player)
            playing_player.update_heuristic_values(board)
            value = playing_player.heuristical_value
        else:
            value = alpha
            playing_player.get_possible_moves(board)
            if (playing_player.possible_moves == []):
                # game ends if both players can't move
                if (moved == False):
                    if (playing_player.colour == 1):
                        coin_difference = board.discs_black - board.discs_white
                    else:
                        coin_difference = board.discs_white - board.discs_black
                    if (coin_difference > 0):
                        value = coin_difference + self.max_heuristic_val
                    else:
                        value = coin_difference + self.min_heuristic_val
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