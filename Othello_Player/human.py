import othello_player.player as player
import pygame

class Human(player.Player):
    def __init__(self,colour, graphical_interface):
        super().__init__(colour)
        self.graphical_interface = graphical_interface

    def make_move(self,board):
        quit_val = False
        made_move = True
        self.get_possible_moves(board)
        if(self.possible_positions == []):
            print('no move possible')
            made_move = False
            return quit_val, made_move, board
        self.graphical_interface.draw_possible_positions(self.possible_positions, self.colour)
        selected_position = None
        while True:
            position = self.graphical_interface.get_mouse_position()
            if(position[0] == 100):
                quit_val = True
                made_move = False
                pygame.quit()
                return True, False, board
            if(position == selected_position):
                break
            elif(position in self.possible_positions):
                selected_position = position
                self.graphical_interface.draw_selected_position(selected_position)
        index = self.possible_positions.index(selected_position)
        return quit_val, made_move,self.possible_moves[index]
