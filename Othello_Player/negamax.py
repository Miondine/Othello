import othello_player.heuritics as heuristics
from copy import deepcopy

class Negamax(heuristics.Heuristic):

    def __init__(self, colour, graphical, graphical_interface):
        super().__init__(colour, graphical ,graphical_interface)
        self.max_depth = 4

    def make_move(self,board):

        self.update_heuristic_values

        max_player = heuristics.Heuristic(self.colour, False, None)
        min_player = heuristics.Heuristic(self.opponent_colour, False, None)

        self.get_possible_moves(board)
        if(self.possible_moves == []):
            return False, board
        else:
            values = []
            for move in self.possible_moves:
                values.append(- self.get_negamax_value(move, min_player, max_player, 1, True))
            max_value = max(values)
            index_max_value = values.index(max_value)
            return True, self.possible_moves[index_max_value]

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
            values = []
            for move in self.possible_moves:
                values.append( - self.get_negamax_value(move, min_player, max_player, 1, True))
            max_value = max(values)
            index_max_value = values.index(max_value)
            return quit_val, True, self.possible_positions[index_max_value], self.possible_moves[index_max_value]


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


    def get_negamax_value(self,board, playing_player, waiting_player,depth, moved):
        # board full, game ends
        if(board.empty_positions == 0):
            playing_player.update_coin_parity(board)
            value = playing_player.coin_parity
            if (value > 0):
                value = value + 100
            else:
                value = value - 100
        elif(depth == self.max_depth):
            self.reset_stability(playing_player)
            playing_player.update_heuristic_values(board)
            value = playing_player.heuristical_value
        else:
            playing_player.get_possible_moves(board)
            if (playing_player.possible_moves == []):
                # game ends if both players can't move
                if (moved == False):
                    playing_player.update_coin_parity(board)
                    value = playing_player.coin_parity
                    if (value > 0):
                        value = value + 100
                    else:
                        value = value - 100
                # no moves possible next players turn
                else:
                    value = - self.get_negamax_value(board, waiting_player, playing_player, depth+1, False)
            else:
                # go one step further in the tree for all possible moves
                values = []
                for move in playing_player.possible_moves:
                    values.append( - self.get_negamax_value(move, waiting_player, playing_player, depth+1 , True))
                value = max(values)
        return value            