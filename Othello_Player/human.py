import othello_player.player as p
import pygame

class Human(p.Player):
    def __init__(self,colour, graphical_interface):
        super().__init__(colour)
        self.graphical_interface = graphical_interface

    def make_move(self,board):
        self.get_possible_moves(board)
        self.graphical_interface.draw_possible_positions(self.possible_positions, self.colour)
        selected_position = None
        while True:
            position = self.graphical_interface.get_mouse_position()
            if(position[0] == 100):
                pygame.quit()
                return 1, board
            if(position == selected_position):
                break
            elif(position in self.possible_positions):
                selected_position = position
                self.graphical_interface.draw_selected_position(selected_position)
        index = self.possible_positions.index(selected_position)
        return 0, self.possible_moves[index]
