from othello_player import player as player
from othello_game import game as game
from copy import deepcopy
import numpy as np
import random


class Node:

    node_counter = 0

    def __init__(self,board,parent,colour):
        self.board_state = board
        self.colour = colour
        self.parent = parent # parent node, None if root node
        self.playing_player = player.Player(colour,False,None)
        self.terminal = False # False if non-terminal node, else True
        self.winner = None
        self.moved = True
        self.playing_player.get_possible_moves(board)
        self.untried_moves = deepcopy(self.playing_player.possible_moves) # possible moves from node, not yet tried
        self.terminal = self.check_terminal() # False if non-terminal node, else True, also changes moved to false if no possible moves
        self.fully_expanded = False # True if all chil nodes have been visited
        self.children = [] # list of all child nodes
        #statistical values of node
        self.q_value = 0
        self.number_visits = 0
        self.name = {f'{Node.node_counter}'}
        Node.node_counter += 1


    def check_terminal(self):
        if(self.board_state.empty_positions == 0):
            if(self.board_state.discs_black > self.board_state.discs_white):
                self.winner = 1
            elif(self.board_state.discs_white > self.board_state.discs_black):
                self.winner = -1
            else:
                self.winner = 0
            return True
        elif(self.untried_moves == []):
            self.moved = False
            if(self.parent != None):
                if(self.parent.moved == False):
                    self.terminal = True
                    if(self.board_state.discs_black > self.board_state.discs_white):
                        self.winner = 1
                    elif(self.board_state.discs_white > self.board_state.discs_black):
                        self.winner = -1
                    else:
                        self.winner = 0
                return True
        return False

class MCTSMaxIterRemember(player.Player):

    def __init__(self, colour, graphical, graphical_interface):
        super().__init__(colour, graphical ,graphical_interface)
        self.max_iterations = 30 # maximum number of iterations
        self.root_node = None

    def make_move(self,board):

        # if no root node exists or root node has no children yet initialise new root node
        if(self.root_node == None or self.root_node.children == []):

            self.root_node = Node(board,None,self.colour)
 
        else:
            # find right old node as new root node to rember old tree
            found_root = False
            for child in self.root_node.children:
                if(child.board_state.positions == board.positions):
                    self.root_node = child
                    self.root_node.parents = None
                    found_root = True
            # if root node not found initialise new root node
            if(found_root == False):
                self.root_node = Node(board,None,self.colour)
                
        if(self.root_node.moved == False):
            return False, board
        elif(len(self.root_node.untried_moves) == 1 and self.root_node.children == []):
            return True, self.root_node.untried_moves[0]
        elif(self.root_node.untried_moves == [] and len(self.root_node.children) == 1):
            return True, self.root_node.children[0].board_state
        
        while(self.root_node.number_visits < self.max_iterations):
            rollout_node = self.tree_policy()
            reward = self.rollout(rollout_node)
            self.backpropagate(rollout_node,reward)

        # for all children of root_node save q_value and number of vistist to choose best child
        child_n_values = []
        child_q_values = []
        for child in self.root_node.children:
            child_n_values.append(child.number_visits)
            child_q_values.append(- child.q_value)
        
        # find list of indices of children with highest number of visits (most robust child)
        max_n_value = max(child_n_values)
        max_n_value_indices = [index for index, value in enumerate(child_n_values) if value == max_n_value]
        # if only one child has highest value return board state of that child
        if(len(max_n_value_indices) == 1):
            self.root_node = self.root_node.children[max_n_value_indices[0]]
            return True, self.root_node.board_state 
        # if more children have highst number of vistist return one randomly chosen child of them with the highest negativ q_value
        else:
            max_nq_values =  [child_q_values[index] for index in max_n_value_indices]
            max_nq_value = max(max_nq_values)
            max_nq_value_indices = [index for index, value in enumerate(max_nq_values) if value == max_nq_value]
            self.root_node = self.root_node.children[max_n_value_indices[random.choice(max_nq_value_indices)]]
            return True, self.root_node.board_state

    def make_move_graphical(self,board):

        quit_val = False
        # if no root node exists or root node has no children yet initialise new root node
        if(self.root_node == None or self.root_node.children == []):

            self.root_node = Node(board,None,self.colour)
 
        else:
            # find right old node as new root node to rember old tree
            found_root = False
            for child in self.root_node.children:
                if(child.board_state.positions == board.positions):
                    self.root_node = child
                    self.root_node.parents = None
                    found_root = True
            # if root node not found initialise new root node
            if(found_root == False):
                self.root_node = Node(board,None,self.colour)
                
        if(self.root_node.moved == False):
            return quit_val,False,[0,0] ,board
        elif(len(self.root_node.untried_moves) == 1 and self.root_node.children == []):
            return quit_val,True,self.root_node.playing_player.possible_positions[0] ,self.root_node.untried_moves[0]
        elif(self.root_node.untried_moves == [] and len(self.root_node.children) == 1):
            return quit_val,True, self.root_node.playing_player.possible_positions[0],self.root_node.children[0].board_state
        
        while(self.root_node.number_visits < self.max_iterations):
            rollout_node = self.tree_policy()
            reward = self.rollout(rollout_node)
            self.backpropagate(rollout_node,reward)

        # for all children of root_node save q_value and number of vistist to choose best child
        child_n_values = []
        child_q_values = []
        for child in self.root_node.children:
            child_n_values.append(child.number_visits)
            child_q_values.append(- child.q_value)
        
        # find list of indices of children with highest number of visits (most robust child)
        max_n_value = max(child_n_values)
        max_n_value_indices = [index for index, value in enumerate(child_n_values) if value == max_n_value]
        # if only one child has highest value return board state of that child
        if(len(max_n_value_indices) == 1):
            position = self.root_node.playing_player.possible_positions[max_n_value_indices[0]]
            self.root_node = self.root_node.children[max_n_value_indices[0]]
            return quit_val,True, position,self.root_node.board_state 
        # if more children have highst number of vistist return one randomly chosen child of them with the highest negativ q_value
        else:
            max_nq_values =  [child_q_values[index] for index in max_n_value_indices]
            max_nq_value = max(max_nq_values)
            max_nq_value_indices = [index for index, value in enumerate(max_nq_values) if value == max_nq_value]
            chosen_child = self.root_node.children[max_n_value_indices[random.choice(max_nq_value_indices)]]
            # find position that lead to child board state:
            for index,move in enumerate(self.root_node.playing_player.possible_moves):
                if(move.positions == chosen_child.board_state.positions):
                    position = self.root_node.playing_player.possible_positions[index]
            self.root_node = chosen_child
            return quit_val, True, position,self.root_node.board_state

    # go down the game tree until either a terminal node is reached or a new node               
    def tree_policy(self):

        current_node = self.root_node

        while(current_node.terminal == False):

            if(current_node.fully_expanded == False):

                # node has no possible moves create child node for opponent player with same board_state (if node would be terminal wouldn't reach this part of code, no deed to check again)
                if(current_node.moved == False):
                    child_node = Node(current_node.board_state,current_node,-current_node.colour)
                    current_node.children.append(child_node)
                    current_node.fully_expanded == True
                    return child_node
                else:
                    child_node = Node(current_node.untried_moves.pop(),current_node,-current_node.colour)
                    current_node.children.append(child_node)
                    if(current_node.untried_moves == []):
                        current_node.fully_expanded = True
                    return child_node

            else:
                current_node = self.best_child(current_node)
   
        return current_node

    # finish game from board state of start node.
    def rollout(self,start_node):

        if(start_node.terminal == True):
            if(start_node.winner == start_node.colour):
                return 1
            elif(start_node.winner == -start_node.colour):
                return -1
            else:
                return 0
        else:
            # if last nodes player could not move need to cheack if following board state is terminal because game object would not catch it.
            if(start_node.moved == False):
                child_node = Node(start_node.board_state,start_node,-start_node.colour)
                if(child_node.terminal == True):
                    if(child_node.winner == start_node.colour):
                        return 1
                    elif(child_node.winner == -start_node.colour):
                        return -1
                    else:
                        return 0
            else:
                #game will start with black to move --> simulate already one move if white is next to move
                if(start_node.colour == -1):
                    name_player1 = 'opponent'
                    name_player2 = 'self'
                    if(start_node.moved == False):
                        board_state = start_node.board_state
                    else:
                        board_state = random.choice(start_node.playing_player.possible_moves)
                else:
                    board_state = start_node.board_state
                    name_player2 = 'opponent'
                    name_player1 = 'self'
                
                #initialise game between two Random player
                random_game = game.Game('GAMBLER',name_player1,'GAMBLER',name_player2,False)
                random_game.game_board = board_state
                random_game.run_game()

                if(random_game.winner == 'self'):
                    return 1
                elif(random_game.winner == 'opponent'):
                    return -1  
                else:
                    return 0            

    def backpropagate(self,current_node, reward):
        current_node.number_visits += 1
        current_node.q_value += reward
        if(current_node.parent != None):
            self.backpropagate(current_node.parent, -reward)

    def best_child(self,current_node):

        weights = []
        for child in current_node.children:
            weights.append(-child.q_value/child.number_visits + np.sqrt(2 * np.log(current_node.number_visits / child.number_visits)))
        max_value = max(weights)
        return current_node.children[weights.index(max_value)]
        

        