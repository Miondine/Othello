import othello_player.player as player
import othello_game.board as board
import othello_game.constants as c
from copy import deepcopy



class Heuristic(player.Player):

    # calls __init__(colour) to initialise player attributes. Initialises stability board with None at all positions. 
    # Input: colour (int)
    def __init__(self, colour):
        super().__init__(colour)
        # stability boards save the status of the disks, None if no own disk is at the position, 1 if stable diks, -1 if not stable, 0 if semi stable
        self.stability_board = [[0 for col in range(c.NUM_COLS)] for row in range(c.NUM_ROWS)] 
        self.opponent_stability_board = [[0 for col in range(c.NUM_COLS)] for row in range(c.NUM_ROWS)]
        # full_rows/cols/diagonals saves if row, col, diagonal of board is fully occupied on board
        self.s_positions = False
        self.full_rows = [False for row in range(c.NUM_ROWS)]
        self.full_cols = [False for col in range(c.NUM_COLS)]
        self.full_right_diagonals = [False for dia in range(c.NUM_DIAGONALS)]
        self.full_left_diagonals = [False for dia in range(c.NUM_DIAGONALS)]
        # saved valid and potential positions for player and opponent
        self.valid_positions = []
        self.potential_positions = []
        self.opponent_valid_positions = []
        self.opponent_potential_positions = []
        # heuritical values
        self.mobility = 0
        self.coin_parity = 0
        self.stability = 0
        self.corners = 0
    
    def update_heuristic_values(self, board):

        self.next_moves(board)
        self.update_coin_parity(board)
        self.update_mobility()
        self.update_corners(board)
        self.update_stability_boards(board)
        self.update_stability(board)

    def next_moves(self, board):

        directions = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]

        for row in range(board.num_rows):
            for col in range(board.num_cols):
                if(board.positions[row][col] != 0):
                        continue
                else:

                    own_valid_position = False
                    opponent_valid_position = False
                    own_potential_position = False
                    opponent_potential_position = False

                    for direction in directions:
                        # check if own position
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
                                own_valid_position = True
                                for temp_row, temp_col in zip(temp_rows,temp_cols):
                                    self.opponent_stability_board[temp_row][temp_col] = -1
                                break  
                            #case five
                            break
                            
                        if(counter > 1):
                            own_potential_position = True
                        
                        # check if opponent position
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
                            elif(board.positions[row+direction[0]*counter][col+direction[1]*counter] == self.colour): 
                                temp_rows.append(row+direction[0]*counter)
                                temp_cols.append(col+direction[1]*counter)
                                counter +=1
                                continue
                            # case four
                            elif(board.positions[row+direction[0]*counter][col+direction[1]*counter] == self.opponent_colour and counter > 1): 
                                opponent_valid_position = True
                                for temp_row, temp_col in zip(temp_rows,temp_cols):
                                    self.stability_board[temp_row][temp_col] = -1
                                break  
                            #case five
                            break

                        if(counter > 1):
                            opponent_potential_position = True

                    # save results for position
                    if own_potential_position:
                        self.potential_positions.append([row,col])
                    if opponent_potential_position:
                        self.opponent_potential_positions.append([row,col])
                    if own_valid_position:
                        self.valid_positions.append([row,col])
                    if opponent_valid_position:
                        self.opponent_valid_positions.append([row,col])
    
    def update_coin_parity(self, board):

        if(self.colour == 1):
            
            self.coin_parity = 100 * (board.disks_white - board.disks_black) / (board.disks_white + board.disks_black)

        else:
                
            self.coin_parity = 100 *  (board.disks_black - board.disks_white) / (board.disks_white + board.disks_black)

    def update_mobility(self):
        
        own_potential_mobility = len(self.potential_positions)
        opponent_potential_mobility = len(self.opponent_potential_positions)
        opponent_current_mobility = len(self.opponent_valid_positions)
        own_current_mobility = len(self.valid_positions)

        # calculate current mobilit value
        if (own_current_mobility + opponent_current_mobility == 0):
            current_mobility = 0
        else:
            current_mobility = 100 *(own_current_mobility - opponent_current_mobility)/(own_current_mobility + opponent_current_mobility)

        # calculate potential mobility value
        if (own_potential_mobility + opponent_potential_mobility == 0):
            potential_mobility = 0
        else:
            potential_mobility = 100 * (own_potential_mobility - opponent_potential_mobility)/(own_potential_mobility + opponent_potential_mobility)       

        # mobility is average between current and potential mobility
        self.mobility = 0.5 * (current_mobility + potential_mobility)

    def update_corners(self, board):
        own_corners = 0
        opponent_corners = 0
        own_corner_adjecents = 0
        opponent_corner_adjecents = 0
        
        #check all corners if occupied if not cal num of adjectent disks, for each player
        for row,col,dir_row,dir_col in ((0,0,1,1),(0,7,1,-1),(7,0,-1,1),(7,7,-1,-1)):
            if(board.positions[row][col] == self.colour):
                own_corners += 1
            elif(board.positions[row][col] == self.opponent_colour):
                opponent_corners += 1
            else:
                # check for disks adjecent to empty corners
                for pos in [[row + dir_row, col],[row, col + dir_col],[row + dir_row, col + dir_col]]:
                    if(board.positions[pos[0]][pos[1]] == self.colour):
                        own_corner_adjecents += 1
                    elif(board.positions[pos[0]][pos[1]] == self.opponent_colour):
                        opponent_corner_adjecents += 1 

        if(own_corners + opponent_corners == 0):
            actual_corner_val = 0
        else:
            actual_corner_val = 100 * (own_corners - opponent_corners)/4
        if(own_corner_adjecents+opponent_corner_adjecents == 0):
            corner_adjecent_val = 0
        else:
            corner_adjecent_val = 100 * (opponent_corner_adjecents - own_corner_adjecents)/12
        self.corners = actual_corner_val + corner_adjecent_val
        
    def update_stability_boards(self, board):

        # find all occupied positions, which are not yet saved as stable or unstable for either player.
        own_semi_stable_disks = []
        opponent_semi_stable_disks = []
        for row in range(board.num_rows):
            for col in range(board.num_cols):
                
                if(board.positions[row][col] == 0):
                    continue
                elif(self.stability_board[row][col] == 1 or self.stability_board[row][col] == -1):
                    continue
                elif(self.opponent_stability_board[row][col] == 1 or self.opponent_stability_board[row][col] == -1):
                    continue
                elif(board.positions[row][col] == self.colour):
                    own_semi_stable_disks.append([row,col])
                else:
                    opponent_semi_stable_disks.append([row,col])
        
        if(own_semi_stable_disks == [] and opponent_semi_stable_disks == []):
            return

        # check if one positions necessary for stable disks is already occupied
        if(self.s_positions == False):
            for row,col in ((0,0),(0,1),(1,0),(0,7),(1,7),(0,6),(7,0),(7,1),(6,0),(7,7),(7,6),(6,7)):
                if(board.positions[row][col] != 0):
                    self.s_positions = True
                    break
        
        if(self.s_positions == False):
            return

        # check for new full rows or coloums, diagonals
        for row in range(board.num_rows):
            # if row is not yet marked as full check if now
            row_full = True
            if not self.full_rows[row]:
                for entry in board.positions[row]:
                    if(entry == 0):
                        row_full = False
                        break
                if(row_full == True):
                    self.full_rows[row] = True
        for col in range(board.num_cols):
            # if col is not yet marked as full check if now
            col_full = True
            if not self.full_cols[col]:
                for row in range(board.num_rows):
                    if(board.positions[row][col] == 0):
                        col_full = False
                        break
                if col_full:
                    self.full_cols[col] = True

        # first 7 left diagonals        
        start_row = 0
        for diagonal, start_col, length in zip(range(0,7,1),range(6,-1,-1),range(2,9,1)):
            # if diagonal is not yet marked as full check if now
            if not self.full_left_diagonals[diagonal]:
                diagonal_full = True
                for row,col in zip(range(start_row,start_row + length,1),range(start_col, start_col + length,1)):
                    if(board.positions[row][col] == 0):
                        diagonal_full = False
                        break
                if diagonal_full:
                    self.full_left_diagonals[diagonal] = True

        # second 6 left diagonals
        start_col = 0
        for diagonal, start_row, length in zip( range(7,13,1), range(1,7,1), range(7,1,-1)):
            # if diagonal is not yet marked as full check if now
            if not self.full_left_diagonals[diagonal]:
                diagonal_full = True
                for row,col in zip(range(start_row,start_row + length,1),range(start_col, start_col + length,1)):
                    if(board.positions[row][col] == 0):
                        diagonal_full = False
                        break
                if diagonal_full:
                    self.full_left_diagonals[diagonal] = True

        # first 7 right diagonals
        start_row = 0
        for diagonal, start_col, length in zip(range(0,7,1),range(1,8,1),range(2,9,1)):
            # if diagonal is not yet marked as full check if now
            if not self.full_right_diagonals[diagonal]:
                diagonal_full = True
                for row,col in zip(range(start_row,start_row + length,1),range(start_col, start_col - length,-1)):
                    if(board.positions[row][col] == 0):
                        diagonal_full = False
                        break
                if diagonal_full:
                    self.full_right_diagonals[diagonal] = True

        # second 6 right diagonals
        start_col = 7
        for diagonal, start_row, length in zip( range(7,13,1), range(1,7,1), range(7,1,-1)):
            # if diagonal is not yet marked as full check if now
            if not self.full_right_diagonals[diagonal]:
                diagonal_full = True
                for row,col in zip(range(start_row,start_row + length,1),range(start_col, start_col - length,-1)):
                    if(board.positions[row][col] == 0):
                        diagonal_full = False
                        break
                if diagonal_full:
                    self.full_right_diagonals[diagonal] = True

        # check if own semi stable disk are stable disk.
        counter = 0
        while True:
            counter += 1
            old_own_semi_stable_disks = deepcopy(own_semi_stable_disks)
            for disk in old_own_semi_stable_disks:
                row_stable = False
                col_stable = False
                diagonal_left_stable = False
                diagonal_right_stable = False
                # if corner then stable
                if disk in [[0,0],[0,7],[7,0],[7,7]]:
                    self.stability_board[disk[0]][disk[1]] = 1
                    own_semi_stable_disks.remove(disk)
                    continue
                # if disk in col 0 or 7 diks cant be flipped in row or diagonal direction
                if(disk[1] == 0 or disk[1] == 7):
                    row_stable = True
                    diagonal_right_stable = True
                    diagonal_left_stable = True
                # check if in full row, else check if disk adjecent in this row to stable disk
                elif(self.full_rows[disk[0]]):
                    row_stable = True
                else:
                    if(disk[1] < 7):
                        if(self.stability_board[disk[0]][disk[1]+1] == 1):
                            row_stable = True
                    if(disk[1] > 0):
                        if(self.stability_board[disk[0]][disk[1]-1] == 1):
                            row_stable = True
                
                # if row is not stable, then disks not stable
                if not row_stable:
                    continue
                # if disk in col 0 or 7 and row stable direction, then disk is stable
                if(disk[0] == 0 or disk[0] == 7):
                    self.stability_board[disk[0]][disk[1]] = 1
                    own_semi_stable_disks.remove(disk)
                    continue
                # check if in full col, else check if disk adjecent in this col to stable disk
                if(self.full_cols[disk[1]]):
                    col_stable = True
                else:
                    if(disk[0] < 7):
                        if(self.stability_board[disk[0]+1][disk[1]] == 1):
                            col_stable = True
                    if(disk[0] > 0):
                        if(self.stability_board[disk[0]-1][disk[1]] == 1):
                            col_stable = True

                # if col is not stable, then disks not stable
                if not col_stable:
                    continue
                # check if in full right diagonal, else check if disk adjecent in this right diagonal to stable disk
                if(self.full_right_diagonals[disk[0] - 1 + disk[1]]):
                    diagonal_right_stable = True
                else:
                    if(disk[0] > 0 and disk[1] < 7):
                        if(self.stability_board[disk[0] - 1][disk[1] + 1] == 1):
                            diagonal_right_stable = True
                    if(disk[0] < 7 and disk[1] > 0):
                        if(self.stability_board[disk[0] + 1][disk[1] - 1] == 1):
                            diagonal_right_stable = True
                # if right diagonal is not stable, then disks not stable
                if not diagonal_right_stable:
                    continue
                # check if in full left diagonal, else check if disk adjecent in this right diagonal to stable disk
                if(self.full_left_diagonals[disk[0] + 6 - disk[1]]):
                    diagonal_left_stable = True
                else:
                    if( disk[0] > 0 and disk[1] > 0):
                        if(self.stability_board[disk[0] - 1][disk[1] - 1] == 1):
                            diagonal_left_stable = True
                    if(disk[0] < 7 and disk[1] < 7):
                        if(self.stability_board[disk[0] + 1][disk[1] + 1] == 1):
                            diagonal_left_stable = True
                # if right diagonal is not stable, then disks not stable
                if not diagonal_left_stable:
                    continue
                # disks is stable, change stability board accordingly
                self.stability_board[disk[0]][disk[1]] = 1
                own_semi_stable_disks.remove(disk) 
            if (old_own_semi_stable_disks == own_semi_stable_disks):
                break
                
            # check if own semi stable disk are stable disk.
        counter = 0
        while True:
            counter += 1
            old_opponent_semi_stable_disks = deepcopy(opponent_semi_stable_disks)
            for disk in old_opponent_semi_stable_disks:
                row_stable = False
                col_stable = False
                diagonal_left_stable = False
                diagonal_right_stable = False
                # if corner then stable
                if disk in [[0,0],[0,7],[7,0],[7,7]]:
                    self.opponent_stability_board[disk[0]][disk[1]] = 1
                    opponent_semi_stable_disks.remove(disk)
                    continue
                # if disk in col 0 or 7 diks cant be flipped in row or diagonal direction
                if(disk[1] == 0 or disk[1] == 7):
                    row_stable = True
                    diagonal_right_stable = True
                    diagonal_left_stable = True
                # check if in full row, else check if disk adjecent in this row to stable disk
                elif(self.full_rows[disk[0]]):
                    row_stable = True
                else:
                    if(disk[1] < 7):
                        if(self.opponent_stability_board[disk[0]][disk[1]+1] == 1):
                            row_stable = True
                    if(disk[1] > 0):
                        if(self.opponent_stability_board[disk[0]][disk[1]-1] == 1):
                            row_stable = True
                
                # if row is not stable, then disks not stable
                if not row_stable:
                    continue
                # if disk in col 0 or 7 and row stable direction, then disk is stable
                if(disk[0] == 0 or disk[0] == 7):
                    self.opponent_stability_board[disk[0]][disk[1]] = 1
                    opponent_semi_stable_disks.remove(disk)
                    continue
                # check if in full col, else check if disk adjecent in this col to stable disk
                if(self.full_cols[disk[1]]):
                    col_stable = True
                else:
                    if(disk[0] < 7):
                        if(self.opponent_stability_board[disk[0]+1][disk[1]] == 1):
                            col_stable = True
                    if(disk[0] > 0):
                        if(self.opponent_stability_board[disk[0]-1][disk[1]] == 1):
                            col_stable = True

                # if col is not stable, then disks not stable
                if not col_stable:
                    continue
                # check if in full right diagonal, else check if disk adjecent in this right diagonal to stable disk
                if(self.full_right_diagonals[disk[0] - 1 + disk[1]]):
                    diagonal_right_stable = True
                else:
                    if(disk[0] > 0 and disk[1] < 7):
                        if(self.opponent_stability_board[disk[0] - 1][disk[1] + 1] == 1):
                            diagonal_right_stable = True
                    if(disk[0] < 7 and disk[1] > 0):
                        if(self.opponent_stability_board[disk[0] + 1][disk[1] - 1] == 1):
                            diagonal_right_stable = True
                # if right diagonal is not stable, then disks not stable
                if not diagonal_right_stable:
                    continue
                # check if in full left diagonal, else check if disk adjecent in this right diagonal to stable disk
                if(self.full_left_diagonals[disk[0] + 6 - disk[1]]):
                    diagonal_left_stable = True
                else:
                    if( disk[0] > 0 and disk[1] > 0):
                        if(self.opponent_stability_board[disk[0] - 1][disk[1] - 1] == 1):
                            diagonal_left_stable = True
                    if(disk[0] < 7 and disk[1] < 7):
                        if(self.opponent_stability_board[disk[0] + 1][disk[1] + 1] == 1):
                            diagonal_left_stable = True
                # if right diagonal is not stable, then disks not stable
                if not diagonal_left_stable:
                    continue
                # disks is stable, change stability board accordingly
                self.opponent_stability_board[disk[0]][disk[1]] = 1
                opponent_semi_stable_disks.remove(disk) 
            if (old_opponent_semi_stable_disks == opponent_semi_stable_disks):
                break

    def update_stability(self,board):
        opponent_stability_value = sum([sum(row) for row in self.opponent_stability_board])
        print(f'opponent stability vaue: {opponent_stability_value}')
        own_stability_value = sum([sum(row) for row in self.stability_board])
        print(f'own stability value: {own_stability_value}')
        if(opponent_stability_value + own_stability_value == 0):
            self.stability = 0
        else:
            self.stability = 100 * (own_stability_value -opponent_stability_value)/(board.disks_white + board.disks_black)
    
    
