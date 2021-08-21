print('in cnn')
from othello_player import player as player
import numpy as np
import configparser
print('before tensorflow')
from tensorflow.python.framework import ops
print('after tensorflow')
from othello_player.CNN_files.othello_net import *
from othello_player.CNN_files.named_nets import *
from othello_player.CNN_files.training_utils import *
import os
print('done import')


#https://github.com/hlynurd/cnn-othello/blob/e59bac3130c8b8baa7f5e91aceae23faa2d08b22/analysis/supervised/experiment_no_features/named_nets.py
class CNN(player.Player):

    path = '/Users/paula/Documents/Programmieren/project/Othello/othello_player/CNN_files/'

    def __init__(self, colour, graphical, graphical_interface):
        super().__init__(colour, graphical ,graphical_interface)
        self.net = self.init_net()

    
    def init_net(self):
        config = configparser.ConfigParser()
        config.read(f'{CNN.path}config.ini')
        start_eta = config.get("myvars", "start_eta")
        iterations = int(config.get("myvars", "iterations"))
        batch_size = int(config.get("myvars", "batch_size"))
        ops.reset_default_graph()
        self.img_data, train_step, optimizer, ground_truths, loss, self.pred_up, learn_rate, score_out = create_othello_net_10l_3()
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        sess = tf.Session(config=config)
        init_op = tf.global_variables_initializer()
        sess.run(init_op)
        current_model = f'{CNN.path}models/convothello_exp_10l.ckpt'
        saver = tf.train.Saver()
        if os.path.isfile(current_model + ".meta"):
            print("locked and loaded")
            saver.restore(sess, current_model)
        return sess

    def board_to_input(self,board):
        player_board = np.zeros((8,8))
        opponent_board = np.zeros((8,8))
        empties = np.zeros((8,8))

        for row in range(8):
            for col in range(8):
                if(board.positions == self.colour):
                    player_board[row][col] = 1
                elif(board.positions == self.opponent_colour):
                    opponent_board[row][col] = 1
                else:
                    empties[row][col] = 1
        return np.dstack(player_board, opponent_board, empties)

    def make_move(self,board):

        self.get_possible_moves()
        input = board_to_input(board)
        input_batch = [input]
        prediction = self.sess.run(self.pred_up,feed_dict={self.img_data:input_batch})
        print(prediction)
        if(self.possible_moves == []):
            return False,board
        else:
            return True, self.possible_moves[0]