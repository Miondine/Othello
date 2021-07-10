import time

class PlayerTimer:
    
    def __init__(self, player_name, opponent_name,num_games):
        
        self.num_games = num_games
        self.player_name = player_name
        self.opponent_name = opponent_name
        self.start_time = None
        self.game_counter = 1
        self.move_counter = 0
        self.game_time = 0
        self.max_moves = 50
        self.move_time_summed = [0.0 for x in range(self.max_moves)]
        self.move_executed = [0 for x in range(self.max_moves)]
        self.game_time_summed = [0.0 for x in range(self.num_games)]
        self.setup_file()

    def setup_file(self):

        
        self.file_string = f'movetime_{self.player_name}_{self.num_games}_{self.opponent_name}.txt'

        self.file = open(self.file_string,'w')

        self.file.write(f'Contains move time for player {self.player_name}; opponent is {self.opponent_name}\n')
        self.file.write(f'Colums refer to move number, rows to game number\n')

        self.file.write('game,')
        for x in range(1,self.max_moves + 1):
            self.file.write(f'{x},')
        self.file.write(f'total\n')

    def start_game(self):
        self.file.write(f'{self.game_counter},')

    def start_move(self):
        self.start_time = time.perf_counter()
    
    def stop_move(self):

        elapsed_time = time.perf_counter() - self.start_time
        self.move_time_summed[self.move_counter] += elapsed_time
        self.move_executed[self.move_counter] += 1
        self.game_time += elapsed_time
        self.move_counter += 1
        self.file.write(f'{elapsed_time},')

    def stop_game(self):

        while(self.move_counter < self.max_moves):
            self.file.write(f'0.0,')
            self.move_counter += 1
        self.file.write(f'{self.game_time}\n')
        self.game_time_summed[self.game_counter - 1] += self.game_time
        self.game_time = 0
        self.move_counter = 0
        self.game_counter += 1

    def close_file(self):
        self.file.write('\n')
        self.file.write('total time per move x,')
        for x in self.move_time_summed:
            self.file.write(f'{x}, ')
        self.file.write(f'{sum(self.move_time_summed)}\n')
        self.file.write('number move x executed,')
        for x in self.move_executed:
            self.file.write(f'{x},')
        self.file.write(f'{self.num_games}\n')
        self.file.write('average time per move x,')
        for x, y in zip(self.move_time_summed,self.move_executed):
            if(y == 0):
                self.file.write('0.0,')
            else:
                average = x / y
                self.file.write(f'{average},')
        self.file.write(f'{sum(self.move_time_summed)/self.num_games}\n')
        self.file.close()




