import scipy.stats
import numpy as np

class ResultFile:

    def __init__(self,name_player1,name_player2,num_games,num_iter,player1_filename = None, player2_filename = None):

        self.name_player1 = name_player1
        self.name_player2 = name_player2
        
        self.num_games = num_games
        self.num_iter = num_iter

        if(player1_filename != None):
            self.player1_filename = player1_filename
            self.player1_file = True
        else:
            self.player1_file = False
        
        if(player2_filename != None):
            self.player2_filename = player2_filename
            self.player2_file = True
        else:
            self.player2_file = False
        

        # statistical results dictionaries
        self.wins_player1 = {'total' : {'summed':[0 for x in range(num_iter)],
                                        'percentage' : [],
                                        'mean' : 0, 'std' : 0, 'err' : 0},
                             'black' : {'summed':[0 for x in range(num_iter)],
                                        'percentage' : [],
                                        'mean' : 0, 'std' : 0, 'err' : 0},
                             'white' : {'summed':[0 for x in range(num_iter)],
                                        'percentage' : [],
                                        'mean' : 0, 'std' : 0, 'err' : 0}}
        self.wins_player2 = {'total' : {'summed':[0 for x in range(num_iter)],
                                        'percentage' : [],
                                        'mean' : 0, 'std' : 0, 'err' : 0},
                             'black' : {'summed':[0 for x in range(num_iter)],
                                        'percentage' : [],
                                        'mean' : 0, 'std' : 0, 'err' : 0},
                             'white' : {'summed':[0 for x in range(num_iter)],
                                        'percentage' : [],
                                        'mean' : 0, 'std' : 0, 'err' : 0}}
        self.discs_player1 = {'total' : {'summed':[0 for x in range(num_iter)],
                                                   'percentage' : [0 for x in range(num_iter)],
                                                   'mean' : 0, 'std' : 0, 'err' : 0},
                                        'black' : {'summed':[0 for x in range(num_iter)],
                                                   'percentage' : [0 for x in range(num_iter)],
                                                   'mean' : 0, 'std' : 0, 'err' : 0},
                                        'white' : {'summed':[0 for x in range(num_iter)],
                                                   'percentage' : [0 for x in range(num_iter)],
                                                   'mean' : 0, 'std' : 0, 'err' : 0}}
        self.discs_player2 = {'total' : {'summed':[0 for x in range(num_iter)],
                                                   'percentage' : [0 for x in range(num_iter)],
                                                   'mean' : 0, 'std' : 0, 'err' : 0},
                                        'black' : {'summed':[0 for x in range(num_iter)],
                                                   'percentage' : [0 for x in range(num_iter)],
                                                   'mean' : 0, 'std' : 0, 'err' : 0},
                                        'white' : {'summed':[0 for x in range(num_iter)],
                                                   'percentage' : [0 for x in range(num_iter)],
                                                   'mean' : 0, 'std' : 0, 'err' : 0}}

        self.filename_raw = f'{name_player1}_{name_player2}_{self.num_iter}_{self.num_games}.txt'
        self.filename_stats = f'{name_player1}_{name_player2}_{self.num_iter}_{self.num_games}_stats.txt'

        self.init_files()

    def init_files(self):
        file_raw = open(self.filename_raw,'w')
        file_raw.write(f'Results for game {self.name_player1} against {self.name_player2}\n')
        file_raw.write(f'Each cycle contains {self.num_games} games, where first half of games {self.name_player1} is black and second half {self.name_player2} is black\n')
        file_raw.write(f'Number of cycles: {self.num_iter}\n')
        file_raw.write('In first two columns winner gets 1 looser 0\n')
        file_raw.write('last two columns refers to number of disc each player has at the end of the game\n')
        file_raw.close()
        file_stats = open(self.filename_stats,'w')
        file_stats.write(f'Statistical evaluation for games between {self.name_player1} against {self.name_player2}\n')
        file_stats.write(f'Each cycle contains {self.num_games} games, where first half of games {self.name_player1} is black and second half {self.name_player2} is black\n')
        file_stats.write(f'Number of cycles: {self.num_iter}\n')
        file_stats.write(f'\n')
        file_stats.close()

    def new_cycle(self, cycle_num):

        file_raw = open(self.filename_raw, 'a')
        file_raw.write('\n')
        file_raw.write(f'Cycle: {cycle_num}\n')
        file_raw.write(f'{self.name_player1},{self.name_player2},Discs_{self.name_player1},Discs_{self.name_player2}\n')
        file_raw.close()

    def save_game_result(self,winner,colour_player1,colour_player2,discs_player1, discs_player2,cycle):

        file_raw = open(self.filename_raw,'a')

        if(winner == None):
            file_raw.write(f'0,0,{discs_player1},{discs_player2}\n')
            return
        elif(winner == self.name_player1):
            disc_diff = discs_player1 - discs_player2
            self.wins_player1[colour_player1]['summed'][cycle] += 1
            self.discs_player1[colour_player1]['summed'][cycle] += disc_diff
            self.wins_player1['total']['summed'][cycle] += 1
            self.discs_player1['total']['summed'][cycle] += disc_diff
            file_raw.write(f'1,0,{discs_player1},{discs_player2}\n')      
        else:
            disc_diff = discs_player2 - discs_player1
            self.wins_player2[colour_player2]['summed'][cycle] += 1
            self.discs_player2[colour_player2]['summed'][cycle] += disc_diff
            self.wins_player2['total']['summed'][cycle] += 1
            self.discs_player2['total']['summed'][cycle] += disc_diff
            file_raw.write(f'0,1,{discs_player1},{discs_player2}\n') 

        file_raw.close()

    def calculate_stats(self):

        self.wins_player1['total']['percentage'] = np.asarray(self.wins_player1['total']['summed']) / self.num_games
        self.wins_player1['black']['percentage'] = np.asarray(self.wins_player1['black']['summed']) / (self.num_games * 0.5)
        self.wins_player1['white']['percentage'] = np.asarray(self.wins_player1['white']['summed']) / (self.num_games * 0.5)
        self.wins_player1['total']['mean'] = scipy.stats.tmean(self.wins_player1['total']['percentage'])
        self.wins_player1['black']['mean'] = scipy.stats.tmean(self.wins_player1['black']['percentage'])
        self.wins_player1['white']['mean'] = scipy.stats.tmean(self.wins_player1['white']['percentage'])
        self.wins_player1['total']['std'] = scipy.stats.tstd(self.wins_player1['total']['percentage'])
        self.wins_player1['black']['std'] = scipy.stats.tstd(self.wins_player1['black']['percentage'])
        self.wins_player1['white']['std'] = scipy.stats.sem(self.wins_player1['white']['percentage'])
        self.wins_player1['total']['err'] = scipy.stats.sem(self.wins_player1['total']['percentage'])
        self.wins_player1['black']['err'] = scipy.stats.sem(self.wins_player1['black']['percentage'])
        self.wins_player1['white']['err'] = scipy.stats.sem(self.wins_player1['white']['percentage'])

        self.wins_player2['total']['percentage'] = np.asarray(self.wins_player2['total']['summed']) / self.num_games
        self.wins_player2['black']['percentage'] = np.asarray(self.wins_player2['black']['summed']) / (self.num_games * 0.5)
        self.wins_player2['white']['percentage'] = np.asarray(self.wins_player2['white']['summed']) / (self.num_games * 0.5)
        self.wins_player2['total']['mean'] = scipy.stats.tmean(self.wins_player2['total']['percentage'])
        self.wins_player2['black']['mean'] = scipy.stats.tmean(self.wins_player2['black']['percentage'])
        self.wins_player2['white']['mean'] = scipy.stats.tmean(self.wins_player2['white']['percentage'])
        self.wins_player2['total']['std'] = scipy.stats.tstd(self.wins_player2['total']['percentage'])
        self.wins_player2['black']['std'] = scipy.stats.tstd(self.wins_player2['black']['percentage'])
        self.wins_player2['white']['std'] = scipy.stats.tstd(self.wins_player2['white']['percentage'])
        self.wins_player2['total']['err'] = scipy.stats.sem(self.wins_player2['total']['percentage'])
        self.wins_player2['black']['err'] = scipy.stats.sem(self.wins_player2['black']['percentage'])
        self.wins_player2['white']['err'] = scipy.stats.sem(self.wins_player2['white']['percentage'])

        for i in range(self.num_iter):
            if(self.wins_player1['total']['summed'][i] != 0):
                self.discs_player1['total']['percentage'][i] = self.discs_player1['total']['summed'][i] / self.wins_player1['total']['summed'][i]
            else:
                self.discs_player1['total']['percentage'][i] = None
            if(self.wins_player1['black']['summed'][i] != 0):
                self.discs_player1['black']['percentage'][i] = self.discs_player1['black']['summed'][i] / self.wins_player1['black']['summed'][i]
            else:
                self.discs_player1['black']['percentage'][i] = None
            if(self.wins_player1['white']['summed'][i] != 0):
                self.discs_player1['white']['percentage'][i] = self.discs_player1['white']['summed'][i] / self.wins_player1['white']['summed'][i]
            else:
                self.discs_player1['white']['percentage'][i] = None
        self.discs_player1['total']['mean'] = scipy.stats.tmean([val for val in self.discs_player1['total']['percentage'] if val != None])
        self.discs_player1['black']['mean'] = scipy.stats.tmean([val for val in self.discs_player1['black']['percentage'] if val != None])
        self.discs_player1['white']['mean'] = scipy.stats.tmean([val for val in self.discs_player1['white']['percentage'] if val != None])
        self.discs_player1['total']['std'] = scipy.stats.tstd([val for val in self.discs_player1['total']['percentage'] if val != None])
        self.discs_player1['black']['std'] = scipy.stats.tstd([val for val in self.discs_player1['black']['percentage'] if val != None])
        self.discs_player1['white']['std'] = scipy.stats.tstd([val for val in self.discs_player1['white']['percentage'] if val != None])
        self.discs_player1['total']['err'] = scipy.stats.sem([val for val in self.discs_player1['total']['percentage'] if val != None])
        self.discs_player1['black']['err'] = scipy.stats.sem([val for val in self.discs_player1['black']['percentage'] if val != None])
        self.discs_player1['white']['err'] = scipy.stats.sem([val for val in self.discs_player1['white']['percentage'] if val != None])

        for i in range(self.num_iter):
            if(self.wins_player2['total']['summed'][i] != 0):
                self.discs_player2['total']['percentage'][i] = self.discs_player2['total']['summed'][i] / self.wins_player2['total']['summed'][i]
            else:
                self.discs_player2['total']['percentage'][i] = None
            if(self.wins_player2['black']['summed'][i] != 0):
                self.discs_player2['black']['percentage'][i] = self.discs_player2['black']['summed'][i] / self.wins_player2['black']['summed'][i]
            else:
                self.discs_player2['black']['percentage'][i] = None
            if(self.wins_player2['white']['summed'][i] != 0):
                self.discs_player2['white']['percentage'][i] = self.discs_player2['white']['summed'][i] / self.wins_player2['white']['summed'][i]
            else:
                self.discs_player2['white']['percentage'][i] = None
        self.discs_player2['total']['mean'] = scipy.stats.tmean([val for val in self.discs_player2['total']['percentage'] if val != None])
        self.discs_player2['black']['mean'] = scipy.stats.tmean([val for val in self.discs_player2['black']['percentage'] if val != None])
        self.discs_player2['white']['mean'] = scipy.stats.tmean([val for val in self.discs_player2['white']['percentage'] if val != None])
        self.discs_player2['total']['std'] = scipy.stats.tstd([val for val in self.discs_player2['total']['percentage'] if val != None])
        self.discs_player2['black']['std'] = scipy.stats.tstd([val for val in self.discs_player2['black']['percentage'] if val != None])
        self.discs_player2['white']['std'] = scipy.stats.tstd([val for val in self.discs_player2['white']['percentage'] if val != None])
        self.discs_player2['total']['err'] = scipy.stats.sem([val for val in self.discs_player2['total']['percentage'] if val != None])
        self.discs_player2['black']['err'] = scipy.stats.sem([val for val in self.discs_player2['black']['percentage'] if val != None])
        self.discs_player2['white']['err'] = scipy.stats.sem([val for val in self.discs_player2['white']['percentage'] if val != None])


    def save_stats(self):

        file_stats = open(self.filename_stats,'a')

        file_stats.write(f'Win percentage per cycle total:    ,Win percentage per cycle p1 is black:    ,Win percentage per cycle p2 is black\n')
        file_stats.write(f'Cycle,{self.name_player1},{self.name_player2},  Cycle,{self.name_player1},{self.name_player2},   Cycle,{self.name_player1},{self.name_player2}\n')
        for cycle in range(self.num_iter):
            file_stats.write(f"{cycle},{self.wins_player1['total']['percentage'][cycle]},{self.wins_player2['total']['percentage'][cycle]},  ")
            file_stats.write(f"{cycle},{self.wins_player1['black']['percentage'][cycle]},{self.wins_player2['white']['percentage'][cycle]},  ")
            file_stats.write(f"{cycle},{self.wins_player1['white']['percentage'][cycle]},{self.wins_player2['black']['percentage'][cycle]}\n")
        file_stats.write(f"Mean,{self.wins_player1['total']['mean']},{self.wins_player2['total']['mean']},    ")
        file_stats.write(f"Mean,{self.wins_player1['black']['mean']},{self.wins_player2['white']['mean']},    ")
        file_stats.write(f"Mean,{self.wins_player1['white']['mean']},{self.wins_player2['black']['mean']}\n")
        file_stats.write(f"Std,{self.wins_player1['total']['std']},{self.wins_player2['total']['std']},    ")
        file_stats.write(f"Std,{self.wins_player1['black']['std']},{self.wins_player2['white']['std']},    ")
        file_stats.write(f"Std,{self.wins_player1['white']['std']},{self.wins_player2['black']['std']}\n")
        file_stats.write(f"Err,{self.wins_player1['total']['err']},{self.wins_player2['total']['err']},    ")
        file_stats.write(f"Err,{self.wins_player1['black']['err']},{self.wins_player2['white']['err']},    ")
        file_stats.write(f"Err,{self.wins_player1['white']['err']},{self.wins_player2['black']['err']}\n")
        file_stats.write('\n')

        file_stats.write(f'Disc Difference per cycle total:    ,Disc Difference per cycle p1 is black:    ,Disc Difference per cycle p2 is black\n')
        file_stats.write(f'Cycle,{self.name_player1},{self.name_player2},  Cycle,{self.name_player1},{self.name_player2},   Cycle,{self.name_player1},{self.name_player2}\n')
        for cycle in range(self.num_iter):
            file_stats.write(f"{cycle},{self.discs_player1['total']['percentage'][cycle]},{self.discs_player2['total']['percentage'][cycle]},  ")
            file_stats.write(f"{cycle},{self.discs_player1['black']['percentage'][cycle]},{self.discs_player2['white']['percentage'][cycle]},  ")
            file_stats.write(f"{cycle},{self.discs_player1['white']['percentage'][cycle]},{self.discs_player2['black']['percentage'][cycle]}\n")
        file_stats.write(f"Mean,{self.discs_player1['total']['mean']},{self.discs_player2['total']['mean']},    ")
        file_stats.write(f"Mean,{self.discs_player1['black']['mean']},{self.discs_player2['white']['mean']},    ")
        file_stats.write(f"Mean,{self.discs_player1['white']['mean']},{self.discs_player2['black']['mean']}\n")
        file_stats.write(f"Std,{self.discs_player1['total']['std']},{self.discs_player2['total']['std']},    ")
        file_stats.write(f"Std,{self.discs_player1['black']['std']},{self.discs_player2['white']['std']},    ")
        file_stats.write(f"Std,{self.discs_player1['white']['std']},{self.discs_player2['black']['std']}\n")
        file_stats.write(f"Err,{self.discs_player1['total']['err']},{self.discs_player2['total']['err']},    ")
        file_stats.write(f"Err,{self.discs_player1['black']['err']},{self.discs_player2['white']['err']},    ")
        file_stats.write(f"Err,{self.discs_player1['white']['err']},{self.discs_player2['black']['err']}\n")
        file_stats.write('\n')

        file_stats.close()

        if(self.player1_file == True):
            f = open(self.player1_filename,'a')
            f.write(f"{self.name_player2},{self.wins_player1['total']['mean']},{self.wins_player1['total']['std']},{self.wins_player1['total']['err']},")
            f.write(f"{self.discs_player1['total']['mean']},{self.discs_player1['total']['std']},{self.discs_player1['total']['err']}\n")
            f.close()
        
        if(self.player2_file == True):
            f = open(self.player2_filename,'a')
            f.write(f"{self.name_player1},{self.wins_player2['total']['mean']},{self.wins_player2['total']['std']},{self.wins_player2['total']['err']},")
            f.write(f"{self.discs_player2['total']['mean']},{self.discs_player2['total']['std']},{self.discs_player2['total']['err']}\n")
            f.close()