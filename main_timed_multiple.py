import othello_game.game as game
import othello_player.playertimer as playertimer
import result_file as resultfile
import tournament as tournament


# players_simple = ['GREEDY','DYNAMIC_ROXANNE','ROXANNE','GAMBLER']
# players_minimax = ['ALPHA_BETA','NEGAMAX', 'STATIC_BOARD','DYNAMIC_BOARD','EDAX']
# players_mcts = ['MCTS_MAX_ITER','MCTS_REM_MAX_ITER']'
def main():

    num_games = 10 # number of games per cycle
    num_cycles = 5

    type_player1 = 'EDAX'
    name_player1 = 'Edax'
    
    for depth in range(1,6):
        depth_player1 = depth
        opponent_types = ['ALPHA_BETA','STATIC_BOARD','DYNAMIC_BOARD','MCTS_MAX_ITER','MCTS_REM_MAX_ITER','GREEDY','GAMBLER','DYNAMIC_ROXANNE','ROXANNE']
        tournamnet_name = f'Tournament{depth_player1}'

        tournament1 = tournament.Tournament(tournamnet_name,type_player1,name_player1,depth_player1 = depth_player1, opponent_types = opponent_types, num_games = num_games, num_cycles = num_cycles, max_depth=5)
        tournament1.play()

if __name__ == "__main__":
    main()