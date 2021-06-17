'''
This class represents a human player. This class is derived from Player class. A human player 
needs a graphical interface to play. 
'''

import othello_player.player as player
import pygame

class Human(player.Player):

    # Calls __init__(colour) to initialise player attributes, initialises own attributes. 
    # Input: colour (int), graphical_interface (Interaction object). 
    # Changes: self.graphical_interaction
    def __init__(self, colour, graphical, graphical_interface):
        super().__init__(colour, graphical ,graphical_interface)

    # Function handles one move of a human player. First calculates all possible moves. If none
    # is possible returns input board, else draws possible moves on board and get human players
    # mouse click. If player clicks exit returns such that game exits, else draws selected move.
    # If player clicks again on selected position function returns new board state. 
    # Input: board (Board object)
    # Output: quit_val (True if player wants to exit game), made_move (True if player made a
    # move, False if passed), board (new board configuration, or old if player passed)
    def make_move_graphical(self,board):

        quit_val = False
        made_move = True

        self.get_possible_moves(board)

        #no move available
        if(self.possible_positions == []):
            made_move = False
            return quit_val, made_move, board

        # draw possible positions
        self.graphical_interface.draw_possible_positions(self.possible_positions, self.colour)
        selected_position = None

        # get position to move to from player or exit.
        while True:
            position = self.graphical_interface.get_mouse_position()
 
            # player wants to exit game
            if(position[0] == 100):
                quit_val = True
                made_move = False
                pygame.quit()
                return True, False, board
            # player clicked an already selected position, return that position
            if(position == selected_position):
                break

            # player clicked on not yet selected position
            elif(position in self.possible_positions):
                selected_position = position
                self.graphical_interface.draw_board(board)
                self.graphical_interface.draw_possible_positions(self.possible_positions, self.colour)
                self.graphical_interface.draw_selected_position(selected_position)

        # retrun selected board configuartion
        index = self.possible_positions.index(selected_position)
        return quit_val, made_move,self.possible_moves[index]
