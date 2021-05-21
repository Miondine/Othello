import othello_game.game as game

#game1 = game.Game('ROXANNE','Roxanne','GAMBLER','Gambler',True)
#game1.run_game()
#print(f'Winner: {game1.winner}')
#print(f'Number of Disks: {game1.name_player1} : {game1.num_disks_player1}, {game1.name_player2} : {game1.num_disks_player2}')

f = open('Roxanne_Gambler_500.txt', 'w')
f.write('"500 games Roxanne agains Gambler for Roxanne: white and Gambler: black."\n')
f.write('"In first two columns winner gets 1 looser 0"\n')
f.write('\n')
f.write('Roxanne Winning, Gambler Winning, Disks Roxanne, Disks Gambler\n')

for x in range(15000):
    game1 = game.Game('ROXANNE','Roxanne','GAMBLER','Gambler',False)
    game1.run_game()
    if(game1.winner == 'Roxanne'):
        f.write(f'1, 0, {game1.num_disks_player1}, {game1.num_disks_player2} \n')
    elif(game1.winner == 'Gambler'):
        f.write(f'0, 1, {game1.num_disks_player1}, {game1.num_disks_player2} \n')
    else:
        f.write(f'0, 0, {game1.num_disks_player1}, {game1.num_disks_player2} \n')

f.close()

f = open('Gambler_Roxanne_500.txt', 'w')
f.write('"500 games Gambler against Roxanne for Gambler: white and Roxanne: black."\n')
f.write('"In first two columns winner gets 1 looser 0"\n')
f.write('\n')
f.write('Roxanne Winning, Gambler Winning, Disks Roxanne, Disks Gambler\n')

for x in range(15000):
    game1 = game.Game('GAMBLER','Gambler','ROXANNE','Roxanne',False)
    game1.run_game()
    if(game1.winner == 'Roxanne'):
        f.write(f'1, 0, {game1.num_disks_player2}, {game1.num_disks_player1} \n')
    elif(game1.winner == 'Gambler'):
        f.write(f'0, 1, {game1.num_disks_player2}, {game1.num_disks_player1} \n')
    else:
        f.write(f'0, 0, {game1.num_disks_player2}, {game1.num_disks_player1} \n')

f.close()