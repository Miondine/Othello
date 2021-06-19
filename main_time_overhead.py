import othello_game.game as game

#game1 = game.Game('ROXANNE','Roxanne','GAMBLER','Gambler',True)
#game1.run_game()
#print(f'Winner: {game1.winner}')
#print(f'Number of Disks: {game1.name_player1} : {game1.num_disks_player1}, {game1.name_player2} : {game1.num_disks_player2}')

f = open('test1_10.txt', 'w')
f.write('"10 games Negamax agains Roxanne for Negamax: white and Roxanne: black."\n')
f.write('"In first two columns winner gets 1 looser 0"\n')
f.write('\n')
f.write('Negamax Winning, Roxanne Winning, Disks Negamax, Disks Roxanne\n')

for x in range(10):
    #game1 = game.Game('NEGAMAX','Negamax','ROXANNE','Roxanne',False)
    #game1.run_game()
    x = 'Roxanne'
    y = 100
    z = 200
    if(x == 'Roxanne'):
        f.write(f'0, 1, {y}, {z} \n')
    elif(x == 'Negamax'):
        f.write(f'1, 0, {y}, {z} \n')
    else:
        f.write(f'0, 0, {y}, {z} \n')

f.close()

f = open('test2_10.txt', 'w')
f.write('"10 games Roxanne against Negamax for Roxanne: white and Negamax: black."\n')
f.write('"In first two columns winner gets 1 looser 0"\n')
f.write('\n')
f.write('Negamax Winning, Roxanne Winning, Disks Negamax, Disks Roxanne\n')

for x in range(10):
    #game1 = game.Game('ROXANNE','Roxanne','NEGAMAX','Negamax',False)
    #game1.run_game()
    x = 'Roxanne'
    y = 100
    z = 200
    if(x == 'Roxanne'):
        f.write(f'0, 1, {y}, {z} \n')
    elif(x == 'Negamax'):
        f.write(f'1, 0, {y}, {z} \n')
    else:
        f.write(f'0, 0, {y}, {z} \n')

f.close()