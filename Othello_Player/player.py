'''
This class represents a player, it contains functions and attributes all different player types use. 
'''

import othello_game.board as board
from copy import deepcopy

class Player:

    # Initialises player attributes, colour of player is determined by input colour. Colour = 1 if white player, -1 if black player 
    # Input: colour. 
    # Changes: self.colour, self.opponents_colour, self.possible_moves, self.possible_positions.
    def __init__(self,colour, graphical_interface):
        self.colour = colour
        if(self.colour == 1):
            self.opponent_colour = -1
        else:
            self.opponent_colour = 1
        self.graphical_interface = graphical_interface
        self.possible_positions = []
        self.possible_moves = []



            
    # Function calculates all possible moves for the calling player for the input board. Function iterates over all board positions. 
    # For all empty positions it checks whether they could be a valid move or not. Therefore, the function expands from the current position
    # in all possible directions and checks if there is a configuration for flipping. 
    # Possible cases while expanding (Pretend player has colour 1):
    # case one: [1 -1 ... out_of_board] or [1 out of board]
    # case two: [1 -1 ... 0] or [1 0]
    # case three [1 -1 ...]
    # case four: [1 -1 ... 1] 
    # case five: [1 1 ...]
    # If function arrives at case four position is a valid move option, function flips in temporary board the enclosed positions for this direction
    # then expands in the remaining direction. 
    # After expanding in all direction, function checks if position is valid (flipping at least one opponents disk). If it is valid it adds position 
    # to possible_positions and adds temporary board to possible_moves
    # Input: board (Board object) board for which player calculates possible possition
    # Changes: possible_positions, possible_moves

    def get_possible_moves(self,board):
        directions = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
        self.possible_moves = []
        self.possible_positions = []
        
        for row in range(board.num_rows):
            for col in range(board.num_cols):
                if(board.positions[row][col] != 0):
                     continue
                else:
                    possible_board = deepcopy(board)
                    valid_position = False
                    for direction in directions:
                        temp_rows = []
                        temp_cols = []
                        counter = 1
                        while True:
                            # case one
                            if(row+direction[0]*counter < 0 or row+direction[0]*counter >= board.num_rows):     
                                break
                            elif(col+direction[1]*counter < 0 or col+direction[1]*counter >= board.num_cols):     
                                break
                            # case two
                            elif(board.positions[row+direction[0]*counter][col+direction[1]*counter] == 0):   
                                break
                            # case three
                            elif(board.positions[row+direction[0]*counter][col+direction[1]*counter] == self.opponent_colour): 
                                temp_rows.append(row+direction[0]*counter)
                                temp_cols.append(col+direction[1]*counter)
                                counter +=1
                                continue
                            # case four
                            elif(board.positions[row+direction[0]*counter][col+direction[1]*counter] == self.colour and counter > 1): 
                                valid_position = True
                                for temp_row, temp_col in zip(temp_rows,temp_cols):
                                    possible_board.positions[temp_row][temp_col] = self.colour
                                break
                                
                            #case five
                            break

                    if (valid_position == True):
                        possible_board.positions[row][col] = self.colour
                        possible_board.update_num_disks()
                        self.possible_positions.append([row,col])
                        self.possible_moves.append(possible_board)
                    


                            
                                





                
     




