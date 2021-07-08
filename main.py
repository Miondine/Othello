import othello_game.game as game

num_games = 100
type_player1 = 'ALPHA_BETA'
type_player2 = 'ROXANNE'
name_player1 = 'AlphaBeta'
name_player2 = 'Roxanne'

f = open(f'{name_player1}_{name_player2}_{num_games}.txt', 'w')
f.write(f'{num_games} games {name_player1} against {name_player2} for {name_player1}: black and {name_player2}: white.\n')
f.write('"In first two columns winner gets 1 looser 0"\n')
f.write('\n')
f.write(f'{name_player1}_Winning,{name_player2}_Winning,Discs_{name_player1},Discs_{name_player2}\n')

for x in range(num_games):
    game1 = game.Game(type_player1,name_player1,type_player2,name_player2,False)
    game1.run_game()
    if(game1.winner == name_player1):
        f.write(f'1,0,{game1.num_discs_player1},{game1.num_discs_player2}\n')
    elif(game1.winner == name_player2):
        f.write(f'0,1,{game1.num_discs_player1},{game1.num_discs_player2}\n')
    else:
        f.write(f'0,0,{game1.num_discs_player1},{game1.num_discs_player2}\n')

f.close()

f = open(f'{name_player2}_{name_player1}_{num_games}.txt', 'w')
f.write(f'{num_games} games {name_player2} against {name_player1} for {name_player2}: black and {name_player1}: white.\n')
f.write('"In first two columns winner gets 1 looser 0"\n')
f.write('\n')
f.write(f'{name_player1}_Winning,{name_player2}_Winning,Discs_{name_player1},Discs_{name_player2}\n')

for x in range(num_games):
    game1 = game.Game(type_player2,name_player2,type_player1,name_player1,False)
    game1.run_game()
    if(game1.winner == name_player1):
        f.write(f'1,0,{game1.num_discs_player2},{game1.num_discs_player1}\n')
    elif(game1.winner == name_player2):
        f.write(f'0,1,{game1.num_discs_player2},{game1.num_discs_player1}\n')
    else:
        f.write(f'0,0,{game1.num_discs_player2},{game1.num_discs_player1}\n')

f.close()