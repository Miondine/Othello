import tournament as tournament


# players_simple = ['GREEDY','DYNAMIC_ROXANNE','ROXANNE','GAMBLER']
# players_minimax = ['ALPHA_BETA','NEGAMAX', 'STATIC_BOARD','DYNAMIC_BOARD','EDAX']
# players_mcts = ['MCTS_MAX_ITER','MCTS_REM_MAX_ITER']'
def main():

    num_games = 10 # number of games per cycle
    num_cycles = 5

    type_player1 = 'STATIC_BOARD'
    name_player1 = 'StaticBoard2'
    depth_player1 = 7
    opponent_types = ['DYNAMIC_ROXANNE']
    tournamnet_name = f'Tournament_1'

    tournament1 = tournament.Tournament(tournamnet_name,type_player1,name_player1,depth_player1 = depth_player1, opponent_types = opponent_types, num_games = num_games, num_cycles = num_cycles)
    tournament1.play()

if __name__ == "__main__":
    main()