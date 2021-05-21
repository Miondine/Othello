import othello_game.game as game

game1 = game.Game('ROXANNE','Roxanne','HUMAN','Axel',True)
game1.run_game()
print(f'Winner: {game1.winner}')
print(f'Number of Disks: {game1.name_player1} : {game1.num_disks_player1}, {game1.name_player2} : {game1.num_disks_player2}')