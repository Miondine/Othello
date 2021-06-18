import time

class PlayerTimer:
    
    def __init__(self, player_name, num_games, colour):
        
        self.num_games = num_games
        self.player_name = player_name
        self.start_time = None
        self.move_time_summed = [0 for x in range(50)]
        self.game_time_summed = [0 for x in range(num_games)]
        self.game_counter = 1
        self.move_counter = 1
        self.game_time = 0
        self.setup_file(colour)

    def setup_file(self, colour):

        if(colour == 1):
            self.file_string = f'movetime_{self.player_name}_{self.num_games}_white.txt'
        else:
            self.file_string = f'movetime_{self.player_name}_{self.num_games}_black.txt'

        self.file = open(self.file_string,'w')

        self.file.write(f'Contains move time for player {player_name}\n')
        self.file.write(f'Colums refer to move numbers, rows to game numer')

        self.file.write('move, ')
        for x in range(50):
            self.file.write(f'{x}, ')
        self.file.write(f'total \n')

    def start_game(self):
        self.file.write(f'game {self.game_counter}, ')

    def start_move(self):
        self.start_time = time.perf_counter()
    
    def stop_move(self):

        elapsed_time = time.perf_counter() - self.start_time
        self.move_time_summed[self.move_counter] += elapsed_time
        self.game_time += elapsed_time
        self.move_counter += 1
        self.file.write(f'{elapsed_time}, ')

    def stop_game(self):

        self.file.write(f'{self.game_time}\n')
        self.game_time_summed[self.game_counter] += self.game_time
        self.game_time = 0
        self.move_counter = 1
        self.game_counter += 1

    def close_file(self):
        self.file.write('total time per move x, ')
        for x in self.move_times:
            self.file.write(f'{x}, ')
        self.file.write(f'{sum(self.move_time_summed)}\n')
        self.file.write('average time per move x, ')
        for x in self.move_time_summed:
            average = x / self.num_games
            self.file.write(f'{average}, ')
        self.file.write(f'{sum(self.move_time_summed)/self.num_games}\n')
        self.file.close()




