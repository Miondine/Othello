import time
import scipy.stats

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
        self.move_time = [[] for x in range(self.max_moves)]
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
        self.move_time[self.move_counter].append(elapsed_time)
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
        for move in range(self.max_moves):
            self.file.write(f'{sum(self.move_time[move])},')
        self.file.write(f'{sum(self.game_time_summed)}\n')

        self.file.write('average time per move x,')
        for move in range(self.max_moves):
            if(len(self.move_time[move]) > 1):
                self.file.write(f'{scipy.stats.tmean(self.move_time[move])},')
            elif(len(self.move_time[move]) == 1):
                self.file.write(f'{self.move_time[move][0]},')
            else:
                self.file.write(f'nan,')
        self.file.write(f'{scipy.stats.tmean(self.game_time_summed)}\n')
        
        self.file.write('std of time per move x,')
        for move in range(self.max_moves):
            if(len(self.move_time[move]) > 1):
                self.file.write(f'{scipy.stats.tstd(self.move_time[move])},')
            else:
                self.file.write('nan,')
        self.file.write(f'{scipy.stats.tstd(self.game_time_summed)}\n')

        self.file.write('err of average time,')
        for move in range(self.max_moves):
            if(len(self.move_time[move]) > 1):
                self.file.write(f'{scipy.stats.sem(self.move_time[move])},')
            else:
                self.file.write('nan,')
        self.file.write(f'{scipy.stats.sem(self.game_time_summed)}\n')

        self.file.close()




