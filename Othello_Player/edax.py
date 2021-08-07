import pexpect
from othello_player import player
from othello_game import constants as c
import random
import os


class Edax(player.Player):

    EXEC_FILE = './bin/mEdax'
    PATH = '/Users/paula/Documents/Programmieren/project/Othello/othello_player/Edax'

    def __init__(self, colour, graphical, graphical_interface, depth):
        super().__init__(colour, graphical ,graphical_interface)
        self.depth = depth
        self.working_dir = os.getcwd()
        self.args = ['-q','-l',f'{self.depth}']
        os.chdir(Edax.PATH)
        self.process = pexpect.spawn(Edax.EXEC_FILE,self.args)
        os.chdir(self.working_dir)


    def make_move(self, board):

        self.get_possible_moves(board)

        if(self.possible_positions == []):
            return False, board
        elif(len(self.possible_positions) == 1):
            return True, self.possible_moves[0]
        
        self.reset(board)
        self.play_move()
        selected_position = self.read_move()
        
        for index,position in enumerate(self.possible_positions):
            if(position == selected_position):
                return True, self.possible_moves[index]

        print('Error: Edax made invalid move')
        index = random.randrange(len(self.possible_positions))
        return True, self.possible_moves[index]

    def make_move_graphical(self,board):

        quit_val = False
        self.get_possible_moves(board)

        if(self.possible_positions == []):
            return quit_val,False, [0,0],board
        elif(len(self.possible_positions) == 1):
            return quit_val, True, self.possible_positions[0],self.possible_moves[0]
        
        self.reset(board)
        self.play_move()
        selected_position = self.read_move()
        
        for index,position in enumerate(self.possible_positions):
            if(position == selected_position):
                return quit_val, True, position,self.possible_moves[index]

        print('Error: Edax made invalid move')
        index = random.randrange(len(self.possible_positions))
        return quit_val, True, self.possible_positions[index], self.possible_moves[index]

    def close_player(self):
        self.close_Edax()

    def reset(self, board):
        s = self.to_edax_str(board, self.colour)
        str = f'setboard {s}'
        self.process.sendline(str)
        # read output from process
        out = self.process.readline(1)
        out = self.process.readline(1)

    def close_Edax(self):
        self.process.sendline('quit')

    def read_move(self):
        
        out = self.process.readline(1)
        encoding = 'utf-8'
        str = out.decode(encoding)
        col = ord(str[11]) - 65
        row = int(str[12]) - 1
        return [row,col]

    def play_move(self):
        self.process.sendline('go')
        out = self.process.readline(1)
        out = self.process.readline(1)
        out = self.process.readline(1)

    def to_edax_str(self, board, player_to_move):
        def to_edax(x):
            if x == 1:
                return 'X'
            elif x == -1:
                return 'O'
            else:
                return '-'

        def gen():
            for row in range(c.NUM_COLS):
                for col in range(c.NUM_COLS):
                    yield to_edax(board.positions[row][col])
            yield ' '
            yield to_edax(player_to_move)

        return ''.join(list(gen()))

    