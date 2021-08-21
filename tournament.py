import othello_game.game as game
import othello_player.playertimer as playertimer
import result_file as resultfile
import othello_game.board as board


class Tournament:

    players_simple = ['GREEDY','DYNAMIC_ROXANNE','ROXANNE','GAMBLER']
    players_minimax = ['ALPHA_BETA','NEGAMAX', 'STATIC_BOARD','DYNAMIC_BOARD','EDAX']
    players_mcts = ['MCTS_MAX_ITER','MCTS_REM_MAX_ITER']
    player_names = {'GREEDY':'Greedy','DYNAMIC_ROXANNE':'DynamicRoxanne','ROXANNE':'Roxanne','GAMBLER':'Gambler',
                    'ALPHA_BETA':'AlphaBeta','NEGAMAX':'Negamax','STATIC_BOARD':'StaticBoard','DYNAMIC_BOARD':'DynamicBoard',
                    'EDAX':'Edax','MCTS_MAX_ITER':'MCTSMaxIter','MCTS_REM_MAX_ITER':'MCTSRemMaxIter'}
    path_init_boardstates = 'initial_game_states.txt'

    def __init__(self, tournament_name, type_player1, name_player1, depth_player1 = None, opponent_types = 'all', opponent_names = None, num_cycles = 10, num_games = 100, min_depth = 1, max_depth = 7, opening_book = False):
        self.tournament_name = tournament_name
        self.type_player1 = type_player1
        if(depth_player1 != None):
            self.name_player1 = f'{name_player1}{depth_player1}'
        else:
            self.name_player1 = name_player1
        self.depth_player1 = depth_player1

        if(opponent_types == 'all'):
            self.opponents_types = ['GREEDY','GAMBLER','ROXANNE','DYNAMIC_ROXANNE','NEGAMAX','ALPHA_BETA','STATIC_BOARD','DYNAMIC_BOARD','MCTS_MAX_ITER','MCTS_REM_MAX_ITER','EDAX']
        else:
            self.opponents_types = opponent_types

        if(opponent_names != None):
            self.opponent_names = opponent_names
        else:
            self.opponent_names = [Tournament.player_names[type] for type in self.opponents_types]
        self.player1_filename = self.init_player_file(self.name_player1)
        self.player2_filename = None
        self.opening_book = opening_book
        self.num_cycles = num_cycles
        self.num_games = num_games
        self.max_depth = max_depth
        self.min_depth = min_depth
        self.mcts_iterations = [50,100,200,500,1000,2000,5000,10000,50000,100000]
        if(type_player1 in Tournament.players_minimax or type_player1 in Tournament.players_mcts):
            self.filename_short = f'tournament_short_{self.name_player1}.txt'
            self.init_file_short()

    def init_file_short(self):

        try:
            f = open(self.filename_short)
            f.close()
            f = open(self.filename_short,'a')
            f.write(f'{self.tournament_name} start\n')
            f.write('\n')
            f.write(f'Opponent,win_black,draw_black,disc_diff_black,win_white,draw_white,disc_diff_white,mean_win,mean_disc_win,mean_disc_loose\n')
            f.close()
        except IOError:
            f = open(self.filename_short,'w')
            f.write(f'Results of games between {self.name_player1} against deterministic opponents. \n')
            f.write(f'First game {self.name_player1} is black and second game opponent is black\n')
            f.write(f'\n')
            f.write(f'{self.tournament_name} start\n')
            f.write('\n')
            f.write(f'Opponent,win_black,draw_black,disc_diff_black,win_white,draw_white,disc_diff_white,mean_win,mean_disc_win,mean_disc_loose\n')
            f.close()

    def close_file(self,filename):
        try:
            f = open(filename)
            f.close()
            f = open(filename,'a')
            f.write(f'\n')
            f.write(f'End of {self.tournament_name}\n')
            f.write(f'\n')
        except:
            return

    def init_player_file(self,name_player):
        
        player_filename = f'{name_player}_results.txt'
        try:
            f = open(player_filename)
            f.close()
            f = open(player_filename,'a')
            f.write(f'{self.tournament_name} start\n')
            f.write('\n')
            f.write(f'opponent,win_percentage,std,err,disc_diff,std,err\n')
            f.close()
        except IOError:
            f = open(player_filename,'w')
            f.write(f'Results of player {name_player} agains different agents\n')
            f.write(f'\n')
            f.write(f'{self.tournament_name} start\n')
            f.write('\n')
            f.write(f'opponent,win_percentage,std,err,disc_diff,std,err\n')
            f.close()

        return player_filename

    def play_stats(self,type_player2, name_player2, depth_player2):

        timer_player1 = playertimer.PlayerTimer(self.name_player1,name_player2, self.num_cycles * self.num_games) 
        timer_player2 = playertimer.PlayerTimer(name_player2,self.name_player1, self.num_cycles * self.num_games)

        player2_filename = self.init_player_file(name_player2)
   
        results = resultfile.ResultFile(self.name_player1,name_player2,self.num_games,self.num_cycles,self.player1_filename,player2_filename)

        for cycle in range(self.num_cycles):
            # print new cycle in output file
            results.new_cycle(cycle)
            # loop over num_games/2 games for player1 black and player2 white
            for game_number in range(int(self.num_games/2)):

                colour_player1 = 'black'
                colour_player2 = 'white'
                # init game
                current_game = game.Game(self.type_player1,self.name_player1,type_player2,name_player2,depth_black = self.depth_player1,depth_white = depth_player2)
                # run game non graphical and timed
                timer_player1.start_game()
                timer_player2.start_game()
                current_game.run_game_timed(timer_player1,timer_player2)
                timer_player1.stop_game()
                timer_player2.stop_game()
                # save result of game
                results.save_game_result(current_game.winner, colour_player1, colour_player2, current_game.num_discs_black, current_game.num_discs_white, cycle)

            # loop over num_games/2 games for player1 white and player2 black
            for game_number in range(int(self.num_games/2)):

                colour_player1 = 'white'
                colour_player2 = 'black'
                # init game
                current_game = game.Game(type_player2,name_player2,self.type_player1,self.name_player1, depth_black = depth_player2,depth_white = self.depth_player1)

                # run game non graphical and timed
                timer_player1.start_game()
                timer_player2.start_game()
                current_game.run_game_timed(timer_player2,timer_player1)
                timer_player1.stop_game()
                timer_player2.stop_game()

                # save result of game
                results.save_game_result(current_game.winner, colour_player1, colour_player2, current_game.num_discs_white, current_game.num_discs_black, cycle)

        results.calculate_stats()
        results.save_stats()
        timer_player1.close_file()
        timer_player2.close_file()
        self.close_file(player2_filename)

    def play(self):

        for type_player2, name_player2 in zip(self.opponents_types,self.opponent_names):

            if(self.type_player1 in Tournament.players_simple): 

                if(type_player2 in Tournament.players_simple):
                    self.play_stats(type_player2,name_player2,depth_player2 = None)
                elif(type_player2 in Tournament.players_minimax):
                    for depth in range(self.min_depth,self.max_depth + 1):
                        self.play_stats(type_player2,f'{name_player2}{depth}',depth_player2 = depth)
                else:
                    for depth in range(self.min_depth - 1,self.max_depth):
                        self.play_stats(type_player2,f'{name_player2}{self.mcts_iterations[depth]}',depth_player2 = self.mcts_iterations[depth])

            else:

                if(type_player2 in Tournament.players_simple):
                    self.play_stats(type_player2,name_player2,depth_player2 = None)
                elif(type_player2 in Tournament.players_minimax):
                    for depth in range(self.min_depth,self.max_depth + 1):
                        if(self.opening_book == True):
                            self.play_stats_opening(type_player2,f'{name_player2}{depth}',depth_player2 = depth)
                        else:
                            self.play_short(type_player2,f'{name_player2}{depth}',depth_player2 = depth)
                else:
                    for depth in range(self.min_depth - 1,self.max_depth):
                        if(self.opening_book == True):
                            self.play_stats_opening(type_player2,f'{name_player2}{self.mcts_iterations[depth]}',depth_player2 = self.mcts_iterations[depth])
                        else:
                            self.play_stats(type_player2,f'{name_player2}{self.mcts_iterations[depth]}',depth_player2 = self.mcts_iterations[depth])

        self.close_file(self.player1_filename)
        self.close_file(self.filename_short)

    def play_short(self,type_player2, name_player2, depth_player2):

        timer_player1 = playertimer.PlayerTimer(self.name_player1,name_player2, 2) 
        timer_player2 = playertimer.PlayerTimer(name_player2,self.name_player1, 2)
        player2_filename = self.init_player_file(name_player2)

        game1 = game.Game(self.type_player1,self.name_player1,type_player2,name_player2,depth_black = self.depth_player1,depth_white = depth_player2)

        timer_player1.start_game()
        timer_player2.start_game()
        game1.run_game_timed(timer_player1,timer_player2)
        timer_player1.stop_game()
        timer_player2.stop_game()

        game2 = game.Game(type_player2,name_player2,self.type_player1,self.name_player1, depth_black = depth_player2,depth_white = self.depth_player1)

        timer_player1.start_game()
        timer_player2.start_game()
        game2.run_game_timed(timer_player2,timer_player1)
        timer_player1.stop_game()
        timer_player2.stop_game()
        
        timer_player1.close_file()
        timer_player2.close_file()

        # save results and calc "stats" 
        discs_win = 0
        discs_loose = 0

        if(game1.winner == self.name_player1):
            win_black = 1
            draw_black = 0
            discs_win += (game1.num_discs_black - game1.num_discs_white)
        elif(game1.winner == name_player2):
            win_black = 0
            draw_black = 0
            discs_loose += (game1.num_discs_black - game1.num_discs_white)
        else:
            win_black = 0
            draw_black = 1

        if(game2.winner == self.name_player1):
            win_white = 1
            draw_white = 0
            discs_win += (game2.num_discs_white - game2.num_discs_black)
        elif(game2.winner == name_player2):
            win_white = 0
            draw_white = 0
            discs_loose += (game2.num_discs_white - game2.num_discs_black)
        else:
            win_white = 0
            draw_white = 1
        
        if(discs_win != 0):
            discs_win = discs_win / (win_black+win_white)
        
        if(discs_loose != 0):
            discs_loose = - discs_loose/(win_white + win_black - 2)

        f = open(self.filename_short,'a')
        f.write(f'{name_player2},{win_black},{draw_black},{game1.num_discs_black-game1.num_discs_white},{win_white},{draw_white},')
        f.write(f'{game2.num_discs_white-game2.num_discs_black},{(win_white + win_black)/2},{discs_win},{discs_loose}\n')
        f.write('\n')
        f.close()
        #opponent,win_percentage,std,err,disc_diff,std,err
        f = open(self.player1_filename, 'a')
        f.write(f'{name_player2},{(win_white+win_black)/2},nan,nan,{discs_win},nan,nan\n')
        f.close()
        f = open(player2_filename,'a')
        f.write(f'{self.name_player1},{1 - (win_white+win_black)/2},nan,nan,{-discs_loose},nan,nan\n')
        f.close()
        self.close_file(player2_filename)

    def play_stats_opening(self,type_player2, name_player2, depth_player2):

        timer_player1 = playertimer.PlayerTimer(self.name_player1,name_player2, self.num_cycles * self.num_games) 
        timer_player2 = playertimer.PlayerTimer(name_player2,self.name_player1, self.num_cycles * self.num_games)

        player2_filename = self.init_player_file(name_player2)
   
        results = resultfile.ResultFile(self.name_player1,name_player2,self.num_games,self.num_cycles,self.player1_filename,player2_filename)

        initial_states = self.read_initial_states()

        for cycle in range(self.num_cycles):
            # print new cycle in output file
            results.new_cycle(cycle)
            # loop over num_games/2 games for player1 black and player2 white
            for game_number in range(int(self.num_games/2)):

                colour_player1 = 'black'
                colour_player2 = 'white'
                # init game
                current_game = game.Game(self.type_player1,self.name_player1,type_player2,name_player2,depth_black = self.depth_player1,depth_white = depth_player2)

                # run game non graphical and timed
                timer_player1.start_game()
                timer_player2.start_game()
                # game will start in game state where 6 moves are already made --> save 3 times 0 move time for each player before starting the game
                for i in range(3):
                    timer_player1.start_move
                    timer_player1.stop_move
                    timer_player2.start_move
                    timer_player2.stop_move
                current_game.game_board = initial_states[int(cycle * self.num_games/2) + game_number]
                current_game.run_game_timed(timer_player1,timer_player2)
                timer_player1.stop_game()
                timer_player2.stop_game()
                # save result of game
                results.save_game_result(current_game.winner, colour_player1, colour_player2, current_game.num_discs_black, current_game.num_discs_white, cycle)

            # loop over num_games/2 games for player1 white and player2 black
            for game_number in range(int(self.num_games/2)):

                colour_player1 = 'white'
                colour_player2 = 'black'
                # init game
                current_game = game.Game(type_player2,name_player2,self.type_player1,self.name_player1, depth_black = depth_player2,depth_white = self.depth_player1)

                # run game non graphical and timed
                timer_player1.start_game()
                timer_player2.start_game()
                # game will start in game state where 6 moves are already made --> save 3 times 0 move time for each player before starting the game
                for i in range(3):
                    timer_player1.start_move
                    timer_player1.stop_move
                    timer_player2.start_move
                    timer_player2.stop_move
                current_game.game_board = initial_states[int(cycle * self.num_games/2) + game_number]
                current_game.run_game_timed(timer_player2,timer_player1)
                timer_player1.stop_game()
                timer_player2.stop_game()

                # save result of game
                results.save_game_result(current_game.winner, colour_player1, colour_player2, current_game.num_discs_white, current_game.num_discs_black, cycle)

        results.calculate_stats()
        results.save_stats()
        timer_player1.close_file()
        timer_player2.close_file()
        self.close_file(player2_filename)

    def read_initial_states(self):

        def to_val(x):
            if x == 'w':
                return -1
            elif x == 'b':
                return 1
            else:
                return 0

        def read_state(line):
            init_board = board.Board()
            for i in range(8):
                for j in range(8):
                    init_board.positions[i][j] = to_val(line[8*i+j])
            return init_board

        def read():
            with open(Tournament.path_init_boardstates, 'r') as f:
                for line in f:
                    yield read_state(line)

        return list(read())


        