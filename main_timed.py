import othello_game.game as game
import othello_player.playertimer as playertimer

num_games = 10
type_player1 = 'ALPHA_BETA'
type_player2 = 'ROXANNE'
name_player1 = 'AlphaBeta'
name_player2 = 'Roxanne'


f = open(f'{name_player1}4_{name_player2}_{num_games}.txt', 'w')
f.write(f'{num_games} games {name_player1} against {name_player2} for {name_player1}: white and {name_player2}: black.\n')
f.write('"In first two columns winner gets 1 looser 0"\n')
f.write('\n')
f.write(f'{name_player1} Winning, {name_player2} Winning, Disks {name_player1}, Disks {name_player2}\n')

player_timer1 = playertimer.PlayerTimer(name_player1,num_games,1)
player_timer2 = playertimer.PlayerTimer(name_player2,num_games,-1)

for x in range(num_games):
    game1 = game.Game(type_player1,name_player1,type_player2,name_player2,False)
    player_timer1.start_game()
    player_timer2.start_game()
    game1.run_game_timed(player_timer1,player_timer2)
    player_timer1.stop_game()
    player_timer2.stop_game()
    if(game1.winner == name_player1):
        f.write(f'1,0, {game1.num_disks_player1}, {game1.num_disks_player2} \n')
    elif(game1.winner == name_player2):
        f.write(f'0, 1, {game1.num_disks_player1}, {game1.num_disks_player2} \n')
    else:
        f.write(f'0, 0, {game1.num_disks_player1}, {game1.num_disks_player2} \n')

player_timer1.close_file()
player_timer2.close_file()

f.close()

f = open(f'{name_player2}_{name_player1}4_{num_games}.txt', 'w')
f.write(f'{num_games} games {name_player2} against {name_player1} for {name_player2}: white and {name_player1}: black.\n')
f.write('"In first two columns winner gets 1 looser 0"\n')
f.write('\n')
f.write(f'{name_player1} Winning, {name_player2} Winning, Disks {name_player1}, Disks {name_player2}\n')

player_timer1 = playertimer.PlayerTimer(name_player2,num_games,1)
player_timer2 = playertimer.PlayerTimer(name_player1,num_games,-1)

for x in range(num_games):
    game1 = game.Game(type_player2,name_player2,type_player1,name_player1,False)
    player_timer1.start_game()
    player_timer2.start_game()
    game1.run_game_timed(player_timer1,player_timer2)
    player_timer1.stop_game()
    player_timer2.stop_game()
    if(game1.winner == name_player1):
        f.write(f'1, 0, {game1.num_disks_player2}, {game1.num_disks_player1} \n')
    elif(game1.winner == name_player2):
        f.write(f'0, 1, {game1.num_disks_player2}, {game1.num_disks_player1} \n')
    else:
        f.write(f'0, 0, {game1.num_disks_player2}, {game1.num_disks_player1} \n')

player_timer1.close_file()
player_timer2.close_file()

f.close()