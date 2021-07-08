import othello_game.game as game

f = open('Negamax4_Roxanne_10.txt', 'w')
f.write('"10 games Negamax agains Roxanne for Negamax: black and Roxanne: white."\n')
f.write('"In first two columns winner gets 1 looser 0"\n')
f.write('\n')
f.write('Negamax_Winning, Roxanne_Winning, Disks_Negamax, Disks_Roxanne\n')

for x in range(10):
    game1 = game.Game('NEGAMAX','Negamax','ROXANNE','Roxanne',False)
    game1.run_game()
    if(game1.winner == 'Roxanne'):
        f.write(f'0, 1, {game1.num_disks_player1}, {game1.num_disks_player2} \n')
    elif(game1.winner == 'Negamax'):
        f.write(f'1, 0, {game1.num_disks_player1}, {game1.num_disks_player2} \n')
    else:
        f.write(f'0, 0, {game1.num_disks_player1}, {game1.num_disks_player2} \n')

f.close()

f = open('Roxanne_Negamax4_10.txt', 'w')
f.write('"10 games Roxanne against Negamax for Roxanne: black and Negamax: white."\n')
f.write('"In first two columns winner gets 1 looser 0"\n')
f.write('\n')
f.write('Negamax_Winning, Roxanne_Winning, Disks_Negamax, Disks_Roxanne\n')

for x in range(10):
    game1 = game.Game('ROXANNE','Roxanne','NEGAMAX','Negamax',False)
    game1.run_game()
    if(game1.winner == 'Roxanne'):
        f.write(f'0, 1, {game1.num_disks_player2}, {game1.num_disks_player1} \n')
    elif(game1.winner == 'Negamax'):
        f.write(f'1, 0, {game1.num_disks_player2}, {game1.num_disks_player1} \n')
    else:
        f.write(f'0, 0, {game1.num_disks_player2}, {game1.num_disks_player1} \n')

f.close()