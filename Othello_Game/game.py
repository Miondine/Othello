import othello_game.board as board
import othello_game.interaction as interaction
import othello_player.player as player
import othello_player.human as human

'''
input: 
typ_player1/2: (String) Typ of player 1/2 one of the following: (HUMAN,ROXANNE)
name_player1/2: (String) name of player1/2
graphical: (Boolean) If true then game will be with graphical output, if false no graphical output.
            If one typ of player is HUMAN then there will be graphical output in either case.

'''
class Game:

    def __init__(self, type_player1, name_player1, type_player2, name_player2, graphical):

        if(graphical or type_player1 == 'HUMAN' or type_player2 == 'HUMAN'):
            self.graphical = True
            self.graphical_interaction = interaction.Interaction()
        else:
            self.graphical = False

        self.player_types = {'HUMAN' : human.Human, 'PLAYER' : player.Player}

        if(type_player1 == 'HUMAN'):
            self.player1 = human.Human(1,self.graphical_interaction)
        else:
            self.player1 = self.player_types[type_player1](1)
        if(type_player2 == 'HUMAN'):
            self.player2 = human.Human(-1,self.graphical_interaction)
        else:
            self.player2 = self.player_types[type_player2](-1)
        
        self.name_player1 = name_player1
        self.name_player2 = name_player2

        self.winner = None
        self.num_disks_player1 = 2
        self.num_disks_player2 = 2
        self.game_board = board.Board()



    def run_game(self):

        if(self.graphical):
            self.run_game_graphical()
        else:
            self.run_game_non_graphical()
    
    def run_game_graphical(self):

        p1_made_move = 0
        p2_made_move = 0
        p1_quit = 0
        p2_quit = 0

        while(self.game_board.empty_positions > 0):

            self.graphical_interaction.draw_board(self.game_board)
            p1_quit, p1_made_move, self.game_board = self.player1.make_move(self.game_board)
            if p1_quit:               
                break
            self.graphical_interaction.draw_board(self.game_board)
            p2_quit, p2_made_move, self.game_board = self.player2.make_move(self.game_board)
            if p2_quit:    
                break
            self.graphical_interaction.draw_board(self.game_board)
            if(not p1_made_move and not p2_made_move):
                if(self.game_board.disks_black > self.game_board.disks_white):
                    self.winner = self.name_player2
                else:
                    self.winner = self.name_player1
                self.num_disks_player2 = self.game_board.disks_black
                self.num_disks_player1 = self.game_board.disks_white
                break
                

            if(self.game_board.empty_positions == 0):
                if(self.game_board.disks_black > self.game_board.disks_white):
                    self.winner = self.name_player2
                else:
                    self.winner = self.name_player1
                self.num_disks_player2 = self.game_board.disks_black
                self.num_disks_player1 = self.game_board.disks_white
                break
                
