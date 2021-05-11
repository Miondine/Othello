import othello_game.constants as c
import othello_game.board as b
from copy import deepcopy

class Player:

    '''
    Each player has a colour (1 (white) or -1 (black)) opponent has the other one. 
    '''
    def __init__(self,colour):
        self.colour = colour
        if(self.colour == 1):
            self.opponent_colour = -1
        else:
            self.opponent_colour = 1
        self.possible_positions = []
        self.possible_moves = []


    '''
    Input: board configuration
            
    Function calculates all possible moves for the calling player for the input board. Function iterates over all board positions. 
    For all empty positions it checks whether they could be a valid move or not. Therefore, the function expands from the current position
    in all possible directions and checks if therer is a configuration for flipping. 

    Possible cases while expanding (Pretend player has colour 1):
    case one: [1 -1 ... out_of_board] or [1 out of board]
    case two: [1 -1 ... 0] or [1 0]
    case three [1 -1 ...]
    case four: [1 -1 ... 1] 
    case five: [1 1 ...]

    If function arrives at case four position is a valid move option, function flipps in temporary board the enclosed positions for this direction
    then expands in the remaining direction. 

    After expanding in all direction, function checks if position is valid (flipping at least one opponents disk). If it is valid it adds position 
    to possible_positions and adds temporary board to possible_moves
    '''
    def get_possible_moves(self,board):
        directions = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
        
        for row in range(c.NUM_ROWS):
            for col in range(c.NUM_COLS):
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
                            if(row+direction[0]*counter < 0 or row+direction[0]*counter >= c.NUM_ROWS):     
                                break
                            elif(col+direction[1]*counter < 0 or col+direction[1]*counter >= c.NUM_COLS):     
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
                        possible_board.update_num_diks()
                        self.possible_positions.append([row,col])
                        self.possible_moves.append(possible_board)
                    

                                
                                
                            
                                





                
     




