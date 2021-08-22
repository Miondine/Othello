import tournament as tournament


# players_simple = ['GREEDY','DYNAMIC_ROXANNE','ROXANNE','GAMBLER']
# players_minimax = ['ALPHA_BETA','NEGAMAX', 'STATIC_BOARD','DYNAMIC_BOARD','EDAX']
# players_mcts = ['MCTS_MAX_ITER','MCTS_REM_MAX_ITER']'
def main():

    num_games = 10 # number of games per cycle
    num_cycles = 10

    type_player1 = 'ALPHA_BETA'
    name_player1 = 'AlphaBeta'
    
    depth_player1 = 1
    opponent_types = ['MCTS_MAX_ITER']
    tournamnet_name = f'Tournament_mcts1'

    tournament1 = tournament.Tournament(tournamnet_name,type_player1,name_player1,depth_player1 = depth_player1, opponent_types = opponent_types, num_games = num_games, num_cycles = num_cycles, max_depth=3)
    tournament1.play()

if __name__ == "__main__":
    main()