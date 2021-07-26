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


class Game:

    # (dic) key: String connected to possible players, value: function for player objects initialisation.
    player_types = {'HUMAN' : human.Human, 'ROXANNE' : roxanne.Roxanne, 'GAMBLER' : gambler.Gambler, 'GREEDY' : greedy.Greedy,
                    'NEGAMAX' : negamax.Negamax, 'ALPHA_BETA' : alphabeta.AlphaBeta, 'STATIC_BOARD' : staticboard.StaticBoard,
                    'DYNAMIC_BOARD' : dynamicBoard.DynamicBoard, 'ROXANNE_DYNAMIC' : roxanneDynamic.RoxanneDynamic,
                    'MCTS_MAX_ITER' : mcts.MCTSMaxIter, 'MCTS_REM_MAX_ITER' : mctsRemember.MCTSMaxIterRemember, 'EDAX': edax.Edax} 
    depth_players = ['NEGAMAX','ALPHA_BETA','STATIC_BOARD','DYNAMIC_BOARD','MCTS_MAX_ITER','MCTS_REM_MAX_ITER','EDAX']

    # initialises object attributes according to input values. 
    # Input: type_player1/2 (string, key to dictionary player_types), name_player1/2 (string, name of player1/2) 
    # Changes: self.graphcial, (self.graphical_interaction), self.name_player1/2, self.type_player1/2, self.num_discs_player1/2, self.winner, self.game_board.
    def __init__(self, type_player1, name_player1, type_player2, name_player2, graphical = None, depth_player1 = None, depth_player2 = None):

        # If at least one player is human or graphcial = True then graphical is True and graphcial_interaction is initialised else graphical is False 
        if(graphical or type_player1 == 'HUMAN' or type_player2 == 'HUMAN'):
            self.graphical = True
            self.graphical_interaction = interaction.Interaction()
            # strings for gui information
            self.turn_player1 = f"{name_player1}'s turn!"
            self.turn_player2 = f"{name_player2}'s turn!"
            self.moved_player1 = f"{name_player1} moved"
            self.moved_player2 = f"{name_player2} moved"
            self.passed_player1 = f"{name_player1} passed"
            self.passed_player2 = f"{name_player2} passsed"
        else:
            self.graphical = False
            self.graphical_interaction = None

        # initialistion of player1/2 according to input variable type_player1/2
        
            if(type_player1 in Game.depth_players):
                self.player1 = Game.player_types[type_player1](colour = 1,graphical = self.graphical, graphical_interface = self.graphical_interaction, depth = depth_player1)
            else:
                self.player1 = Game.player_types[type_player1](colour = 1,graphical = self.graphical, graphical_interface = self.graphical_interaction)
            if(type_player2 in Game.depth_players):
                self.player2 = Game.player_types[type_player2](colour = 1,graphical = self.graphical, graphical_interface = self.graphical_interaction, depth = depth_player2)
            else:
                self.player2 = Game.player_types[type_player2](colour = 1,graphical = self.graphical, graphical_interface = self.graphical_interaction)
            
        
        self.type_player1 = type_player1
        self.type_player2 = type_player2

        # names of players are used for output
        self.name_player1 = name_player1
        self.name_player2 = name_player2

        self.winner = None
        self.num_discs_player1 = 2 # (int) number of discs player 1 has after game was played.
        self.num_discs_player2 = 2 # (int) number of discs player 2 has after game was played.
        self.game_board = board.Board() # (board object) current board object (state of the game).

    def close_game(self):

        self.player1.close_player()
        self.player2.close_player()

    # calls function run_game_graphical() or run_game_non_graphical() depending on the value of self.graphical.
    def run_game(self):

        if(self.graphical):
            self.run_game_graphical()
        else:
            self.run_game_non_graphical()
    
    # simulates one game between player1/2 with graphical output/interaction. loops over turn player1, turn player2 until
    # no more empty positions are available, both players passed or a human player clicked quit. For turn from player1/2 
    # calls player object function make_move_graphical(self.game_board). After each turn draws new board on window. If 
    # player is not human, asks user to click next.
    # Changes: self.game_board, self.winner, self.num_discs_player1/2, self.window
    def run_game_graphical(self):

        # draw board on screen, wait for start click
        self.graphical_interaction.draw_board(self.game_board)
        self.graphical_interaction.draw_start_button()
        quit_val = self.graphical_interaction.get_next_click()               
        if quit_val:
            self.close_game()
            exit()

        
        p1_made_move = True
        p2_made_move = True

        while True:

            self.graphical_interaction.draw_board(self.game_board)
            self.graphical_interaction.display_string(self.turn_player1)
            pygame.time.wait(1000)

            # player1 moves
            p1_quit, p1_made_move, position, self.game_board = self.player1.make_move_graphical(self.game_board)

            # exit game loop if player 2 selected quit
            if p1_quit:               
                self.close_game()
                exit()

            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not p1_made_move and not p2_made_move):
                self.game_finish_graphical()
                break
                
            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish_graphical()
                break

            # draw board on screen and if player moved selected position.
            if p1_made_move:
                self.graphical_interaction.draw_board(self.game_board)
                self.graphical_interaction.display_string(self.moved_player1)
                self.graphical_interaction.draw_selected_position(position)
            else:
                self.graphical_interaction.draw_board(self.game_board)
                self.graphical_interaction.display_string(self.passed_player1)

            # wait until user clicks next
            quit_val = self.graphical_interaction.get_next_click()
            if quit_val:
                self.close_game()
                exit()

            self.graphical_interaction.draw_board(self.game_board)
            self.graphical_interaction.display_string(self.turn_player2)
            pygame.time.wait(1000)

            # player2 moves
            p2_quit, p2_made_move, position, self.game_board = self.player2.make_move_graphical(self.game_board)

            # exit game loop if player 2 selected quit
            if p2_quit:    
                self.close_game()
                exit()

            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not p1_made_move and not p2_made_move):
                self.game_finish_graphical()
                break
                
            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish_graphical()
                break

            # draw board on screen and if player moved selected position 
            if p2_made_move:
                self.graphical_interaction.draw_board(self.game_board)
                self.graphical_interaction.display_string(self.moved_player2)
                self.graphical_interaction.draw_selected_position(position)
            else:
                self.graphical_interaction.draw_board(self.game_board)
                self.graphical_interaction.display_string(self.passed_player2)

            # wait until user clicks next
            quit_val = self.graphical_interaction.get_next_click()
            if quit_val:
                self.close_game()
                exit()



    def game_finish_graphical(self):

        if(self.game_board.discs_black > self.game_board.discs_white):
            self.winner = self.name_player1
            # assign all empty positions to the winner
            self.game_board.discs_black += self.game_board.empty_positions
        elif(self.game_board.discs_black < self.game_board.discs_white):
            self.winner = self.name_player2
            # assign all empty positions to the winner
            self.game_board.discs_white += self.game_board.empty_positions
        self.num_discs_player2 = self.game_board.discs_white
        self.num_discs_player1 = self.game_board.discs_black

        self.graphical_interaction.draw_board(self.game_board)
        self.graphical_interaction.display_string(f"The winner is {self.winner}. {self.name_player1} has {self.num_discs_player1} discs and {self.name_player2} has {self.num_discs_player2} discs")
        # wait until player clicks next button or quit to exit game
        self.graphical_interaction.draw_next_button()
        quit_val = self.graphical_interaction.get_next_click()
        if quit_val:
            self.close_game()
            exit()

    # simulates one game between player1/2. Loops over turn player1, turn player2 until no more empty positions are available or both
    # players passed. For turn from player1/2 calls player object function make_move(self.game_board). 
    # Changes: self.game_board, self.winner, self.num_discs_player1/2.
    def run_game_non_graphical(self):

        p1_made_move = True
        p2_made_move = True
        while True:

            # player1 moves
            p1_made_move, self.game_board = self.player1.make_move(self.game_board)

            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not p1_made_move and not p2_made_move):
                self.game_finish()
                break
                
            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish()
                break

            # player2 moves
            p2_made_move, self.game_board = self.player2.make_move(self.game_board)

            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not p1_made_move and not p2_made_move):
                self.game_finish()
                break
                
            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish()
                break

    def game_finish(self):

        if(self.game_board.discs_black > self.game_board.discs_white):
            self.winner = self.name_player1
            # assign all empty positions to the winner
            self.game_board.discs_black += self.game_board.empty_positions
        elif(self.game_board.discs_black < self.game_board.discs_white):
            self.winner = self.name_player2
            # assign all empty positions to the winner
            self.game_board.discs_white += self.game_board.empty_positions
        self.num_discs_player2 = self.game_board.discs_white
        self.num_discs_player1 = self.game_board.discs_black

    def run_game_timed(self,timer_player1,timer_player2):

        p1_made_move = True
        p2_made_move = True

        while True:

            # player1 moves
            timer_player1.start_move()
            p1_made_move, self.game_board = self.player1.make_move(self.game_board)
            timer_player1.stop_move()

            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not p1_made_move and not p2_made_move):
                self.game_finish()
                break
                
            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish()
                break

            # player2 moves
            timer_player2.start_move()
            p2_made_move, self.game_board = self.player2.make_move(self.game_board)
            timer_player2.stop_move()
            # if both players passed calculate number of diks for each player, determine winner leave game loop
            if(not p1_made_move and not p2_made_move):
                self.game_finish()
                break
                
            # if no more empty positions calculate number of diks for each player, determine winner leave game loop
            if(self.game_board.empty_positions == 0):
                self.game_finish()
                break