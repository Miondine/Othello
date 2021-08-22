'''
Game object represents one game played between two players. Handles main loop over the game, where each player makes a move or passes each round. 
Can either handle a game without graphical output or with. Sets winner and number of discs in the end.
'''

import othello_game.board as board
import othello_game.interaction as interaction
import othello_player.human as human
import othello_player.roxanne as roxanne
import othello_player.gambler as gambler
import othello_player.greedy as greedy
import othello_player.negamax as negamax
import othello_player.alphabeta as alphabeta
import othello_player.staticboard as staticboard
import othello_player.dynamicBoard as dynamicBoard
import othello_player.roxanneDynamic as roxanneDynamic
import othello_player.mcts as mcts
import othello_player.mctsRemember as mctsRemember
import othello_player.edax as edax
import pygame
import random


class Game:

    # (dic) key: String connected to possible players, value: function for player objects initialisation.
    player_types = {'HUMAN' : human.Human, 'ROXANNE' : roxanne.Roxanne, 'GAMBLER' : gambler.Gambler, 'GREEDY' : greedy.Greedy,
                    'NEGAMAX' : negamax.Negamax, 'ALPHA_BETA' : alphabeta.AlphaBeta, 'STATIC_BOARD' : staticboard.StaticBoard,
                    'DYNAMIC_BOARD' : dynamicBoard.DynamicBoard, 'DYNAMIC_ROXANNE' : roxanneDynamic.RoxanneDynamic, 
                    'MCTS_MAX_ITER' : mcts.MCTSMaxIter, 'MCTS_REM_MAX_ITER' : mctsRemember.MCTSMaxIterRemember, 'EDAX': edax.Edax} 
    depth_players = ['NEGAMAX','ALPHA_BETA','STATIC_BOARD','DYNAMIC_BOARD','MCTS_MAX_ITER','MCTS_REM_MAX_ITER','EDAX']

    # initialises object attributes according to input values. 
    # Input: type_black/white (string, key to dictionary player_types), name_black/white (string, name of black/2) 
    # Changes: self.graphcial, (self.graphical_interaction), self.name_black/white, self.type_black/white, self.num_discs_black/2, self.winner, self.game_board.
    def __init__(self, type_black, name_black, type_white, name_white, graphical = None, depth_black = None, depth_white = None):

        # If at least one player is human or graphcial = True then graphical is True and graphcial_interaction is initialised else graphical is False 
        if(graphical or type_black == 'HUMAN' or type_white == 'HUMAN'):
            self.graphical = True
            self.graphical_interaction = interaction.Interaction()
            # strings for gui information
            self.turn_black = f"{name_black}'s turn!"
            self.turn_white = f"{name_white}'s turn!"
            self.moved_black = f"{name_black} moved"
            self.moved_white = f"{name_white} moved"
            self.passed_black = f"{name_black} passed"
            self.passed_white = f"{name_white} passsed"
        else:
            self.graphical = False
            self.graphical_interaction = None

        # initialistion of black/2 according to input variable type_black/white
        
        if(type_black in Game.depth_players):
            self.black = Game.player_types[type_black](colour = 1,graphical = self.graphical, graphical_interface = self.graphical_interaction, depth = depth_black)
        else:
            self.black = Game.player_types[type_black](colour = 1,graphical = self.graphical, graphical_interface = self.graphical_interaction)
        if(type_white in Game.depth_players):
            self.white = Game.player_types[type_white](colour = -1,graphical = self.graphical, graphical_interface = self.graphical_interaction, depth = depth_white)
        else:
            self.white = Game.player_types[type_white](colour = -1,graphical = self.graphical, graphical_interface = self.graphical_interaction)
                  
        self.type_black = type_black
        self.type_white = type_white

        self.name_black = name_black
        self.name_white = name_white

        self.winner = None
        self.num_discs_black = 2 # (int) number of discs black player has after game was played.
        self.num_discs_white = 2 # (int) number of discs white player has after game was played.
        self.game_board = board.Board() # (board object) current board object (state of the game).

    def close_game(self):

        self.black.close_player()
        self.white.close_player()

    # calls function run_game_graphical() or run_game_non_graphical() depending on the value of self.graphical.
    def run_game(self):

        if(self.graphical):
            self.run_game_graphical()
        else:
            self.run_game_non_graphical()
    
    # simulates one game between black/2 with graphical output/interaction. loops over turn black, turn white until
    # no more empty positions are available, both players passed or a human player clicked quit. For turn from black/2 
    # calls player object function make_move_graphical(self.game_board). After each turn draws new board on window. If 
    # player is not human, asks user to click next.
    # Changes: self.game_board, self.winner, self.num_discs_black/2, self.window
    def run_game_graphical(self):

        # draw board on screen, wait for start click
        self.graphical_interaction.draw_board(self.game_board)
        self.graphical_interaction.draw_start_button()
        quit_val = self.graphical_interaction.get_next_click()               
        if quit_val:
            self.close_game()
            exit()

        
        black_made_move = True
        white_made_move = True

        while True:

            self.graphical_interaction.draw_board(self.game_board)
            self.graphical_interaction.display_string(self.turn_black)
            pygame.time.wait(1000)

            # black moves
            black_quit, black_made_move, position, self.game_board = self.black.make_move_graphical(self.game_board)

            # exit game loop if black player selected quit
            if black_quit:               
                self.close_game()
                exit()

            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not black_made_move and not white_made_move):
                self.game_finish_graphical()
                break
                
            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish_graphical()
                break

            # draw board on screen and if player moved selected position.
            if black_made_move:
                self.graphical_interaction.draw_board(self.game_board)
                self.graphical_interaction.display_string(self.moved_black)
                self.graphical_interaction.draw_selected_position(position)
            else:
                self.graphical_interaction.draw_board(self.game_board)
                self.graphical_interaction.display_string(self.passed_black)

            # wait until user clicks next
            quit_val = self.graphical_interaction.get_next_click()
            if quit_val:
                self.close_game()
                exit()

            self.graphical_interaction.draw_board(self.game_board)
            self.graphical_interaction.display_string(self.turn_white)
            pygame.time.wait(1000)

            # white moves
            white_quit, white_made_move, position, self.game_board = self.white.make_move_graphical(self.game_board)

            # exit game loop if black player selected quit
            if white_quit:    
                self.close_game()
                exit()

            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not black_made_move and not white_made_move):
                self.game_finish_graphical()
                break
                
            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish_graphical()
                break

            # draw board on screen and if player moved selected position 
            if white_made_move:
                self.graphical_interaction.draw_board(self.game_board)
                self.graphical_interaction.display_string(self.moved_white)
                self.graphical_interaction.draw_selected_position(position)
            else:
                self.graphical_interaction.draw_board(self.game_board)
                self.graphical_interaction.display_string(self.passed_white)

            # wait until user clicks next
            quit_val = self.graphical_interaction.get_next_click()
            if quit_val:
                self.close_game()
                exit()



    def game_finish_graphical(self):

        if(self.game_board.discs_black > self.game_board.discs_white):
            self.winner = self.name_black
            # assign all empty positions to the winner
            self.game_board.discs_black += self.game_board.empty_positions
        elif(self.game_board.discs_black < self.game_board.discs_white):
            self.winner = self.name_white
            # assign all empty positions to the winner
            self.game_board.discs_white += self.game_board.empty_positions
        self.num_discs_white = self.game_board.discs_white
        self.num_discs_black = self.game_board.discs_black

        self.graphical_interaction.draw_board(self.game_board)
        self.graphical_interaction.display_string(f"The winner is {self.winner}. {self.name_black} has {self.num_discs_black} discs and {self.name_white} has {self.num_discs_white} discs")
        # wait until player clicks next button or quit to exit game
        self.graphical_interaction.draw_next_button()
        quit_val = self.graphical_interaction.get_next_click()
        if quit_val:
            self.close_game()
            exit()

    # simulates one game. Loops over turn black, turn white until no more empty positions are available or both
    # players passed. For turn from black/white calls player object function make_move(self.game_board). 
    # Changes: self.game_board, self.winner, self.num_discs_black/white.
    def run_game_non_graphical(self):

        black_made_move = True
        white_made_move = True
        while True:

            # black moves
            black_made_move, self.game_board = self.black.make_move(self.game_board)

            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not black_made_move and not white_made_move):
                self.game_finish()
                break
                
            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish()
                break

            # white moves
            white_made_move, self.game_board = self.white.make_move(self.game_board)

            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not black_made_move and not white_made_move):
                self.game_finish()
                break
                
            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish()
                break

    def game_finish(self):

        if(self.game_board.discs_black > self.game_board.discs_white):
            self.winner = self.name_black
            # assign all empty positions to the winner
            self.game_board.discs_black += self.game_board.empty_positions
        elif(self.game_board.discs_black < self.game_board.discs_white):
            self.winner = self.name_white
            # assign all empty positions to the winner
            self.game_board.discs_white += self.game_board.empty_positions
        self.num_discs_white = self.game_board.discs_white
        self.num_discs_black = self.game_board.discs_black

    def run_game_timed(self,timer_black,timer_white):

        black_made_move = True
        white_made_move = True      
     
        while True:

            # black moves
            timer_black.start_move()
            black_made_move, self.game_board = self.black.make_move(self.game_board)
            timer_black.stop_move()
            
            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not black_made_move and not white_made_move):
                self.game_finish()
                break

            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish()
                break

            # white moves
            timer_white.start_move()
            white_made_move, self.game_board = self.white.make_move(self.game_board)
            timer_white.stop_move()

            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not black_made_move and not white_made_move):
                self.game_finish()
                break
       
            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish()
                break

    def run_game_timed_random(self,timer_black,timer_white):
        
        black_made_move = True
        white_made_move = True      
        random_white = gambler.Gambler(-1,False,None)
        random_black = gambler.Gambler(1,False,None)
     
        while True:

            # black moves, with 7 % probability black makes random move (should make in average 2 random moves per game)
            r = random.randint(1,100)
            if(r <= 7):
                timer_black.start_move()
                black_made_move, self.game_board = random_black.make_move(self.game_board)
                timer_black.stop_move()
            else:
                timer_black.start_move()
                black_made_move, self.game_board = self.black.make_move(self.game_board)
                timer_black.stop_move()
            
            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not black_made_move and not white_made_move):
                self.game_finish()
                break

            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish()
                break

            # white moves, with 7 % probability white makes random move (should make in average 2 random moves per game)
            r = random.randint(1,100)
            if(r <= 7):
                timer_white.start_move()
                white_made_move, self.game_board = random_white.make_move(self.game_board)
                timer_white.stop_move()
            else:
                timer_white.start_move()
                white_made_move, self.game_board = self.white.make_move(self.game_board)
                timer_white.stop_move()

            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not black_made_move and not white_made_move):
                self.game_finish()
                break
       
            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish()
                break
            