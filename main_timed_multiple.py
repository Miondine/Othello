import othello_game.game as game
import othello_player.playertimer as playertimer
import result_file as resultfile

def init_player_file(player_file_name, name_player):
    player_file = open(player_file_name,'w')
    player_file.write(f'Results of player {name_player} agains different agents\n')
    player_file.write(f'\n')
    player_file.write(f'opponent,win_percentage,std,err,disc_diff,std,err\n')

def main():

    num_games = 100 # number of games per cycle
    num_iter = 10

    type_player1 = 'DYNAMIC_ROXANNE'
    name_player1 = 'DynamicRoxanne'
    depth_player1 = None
    if(depth_player1 != None):
        name_player1 = f"{name_player1}{depth_player1}"

    player1_file_name = f'{name_player1}_results.txt'
    try:
        f = open(player1_file_name)
        f.close()
    except IOError:
        init_player_file(player1_file_name,name_player1)

    second_players_simple = [['GREEDY','Greedy'],['DYNAMIC_ROXANNE','DynamicRoxanne']]#,['ROXANNE','Roxanne'],['GAMBLER','Gambler']]
    second_players_minimax = [['ALPHA_BETA','AlphaBeta'],['NEGAMAX','Negamax'],['STATIC_BOARD','StaticBoard'],['DYNAMIC_BOARD','DynamicBoard'],['EDAX','Edax']]
    second_players_mcts = [['MCTS_MAX_ITER','MCTSMaxIter'],['MCTS_REM_MAX_ITER','MCTSRemMaxIter']]

    # Games against simple agents
    for type_player2,name_player2 in [val for val in second_players_simple if val != [type_player1,name_player1]]:

        player_timer1 = playertimer.PlayerTimer(name_player1,name_player2, num_iter * num_games) 
        player_timer2 = playertimer.PlayerTimer(name_player2,name_player1, num_iter * num_games)

        player2_file_name = f'{name_player2}_results.txt'
        try:
            f = open(player2_file_name)
            f.close()
        except IOError:
            init_player_file(player2_file_name,name_player2)
        results = resultfile.ResultFile(name_player1,name_player2,num_games,num_iter,player1_file_name,player2_file_name)

        for cycle in range(num_iter):
            # print new cycle in output file
            results.new_cycle(cycle)
            # loop over num_games/2 games for player1 black and player2 white
            for game_number in range(int(num_games/2)):

                colour_player1 = 'black'
                colour_player2 = 'white'
                # init game
                current_game = game.Game(type_player1,name_player1,type_player2,name_player2)

                # run game non graphical and timed
                player_timer1.start_game()
                player_timer2.start_game()
                current_game.run_game_timed(player_timer1,player_timer2)
                player_timer1.stop_game()
                player_timer2.stop_game()

                # save result of game
                results.save_game_result(current_game.winner, colour_player1, colour_player2, current_game.num_discs_player1, current_game.num_discs_player2, cycle)

            # loop over num_games/2 games for player1 white and player2 black
            for game_number in range(int(num_games/2)):

                colour_player1 = 'white'
                colour_player2 = 'black'
                # init game
                current_game = game.Game(type_player2,name_player2,type_player1,name_player1)

                # run game non graphical and timed
                player_timer1.start_game()
                player_timer2.start_game()
                current_game.run_game_timed(player_timer2,player_timer1)
                player_timer1.stop_game()
                player_timer2.stop_game()

                # save result of game
                results.save_game_result(current_game.winner, colour_player1, colour_player2, current_game.num_discs_player2, current_game.num_discs_player1, cycle)

        results.calculate_stats()
        results.save_stats()
        player_timer1.close_file()
        player_timer2.close_file()


if __name__ == "__main__":
    main()