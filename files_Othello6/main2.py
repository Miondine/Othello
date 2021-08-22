import tournament as tournament


# players_simple = ['GREEDY','DYNAMIC_ROXANNE','ROXANNE','GAMBLER']
# players_minimax = ['ALPHA_BETA','NEGAMAX', 'STATIC_BOARD','DYNAMIC_BOARD','EDAX']
# players_mcts = ['MCTS_MAX_ITER','MCTS_REM_MAX_ITER']'
def main():

    num_games = 10 # number of games per cycle
    num_cycles = 10

    type_player1 = 'EDAX'
    name_player1 = 'Edax'


    for depth in range(1,5):
        depth_player1 = depth
        opponent_types = ['ALPHA_BETA']
        tournamnet_name = f'Tournament_2'

        tournament1 = tournament.Tournament(tournamnet_name,type_player1,name_player1,depth_player1 = depth_player1, opponent_types = opponent_types, num_games = num_games, num_cycles = num_cycles, min_depth = 5,max_depth=6)
        tournament1.play()

if __name__ == "__main__":
    main()