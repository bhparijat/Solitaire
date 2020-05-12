import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
import unittest
import tqdm.notebook as tq
import solitaire_env
import sys
import seaborn as sns
import pickle as pkl
import gp 
sys.setrecursionlimit(10**6)
number_of_runs = 100
class Collect_data:
    
    def __init__(self,N=100,games_per_run=1000,fp_flag = True,debug=False,save_intermediate_states=False):
        
        self.number_of_runs = N
        
        self.save_collected_data = {}
        self.games_per_run = games_per_run
        
        self.fp_flag = fp_flag
        
        self.debug = debug
        
        self.save_intermediate_states = save_intermediate_states
        
        self.all_runs = {}
        
        self.max_steps_per_game = 100000
    
        self.win_count = []
        
        
    def run_one_episode(self):
         
        wins = 0
        
        
        actions_for_each_game = [0]*self.games_per_run
        iterations_used_per_game = [0]*self.games_per_run
        different_states_per_game = [0]*self.games_per_run
        
        actions_matrix = [0]*self.games_per_run
        
        
        
        for this_game in range(self.games_per_run):
            
            env = solitaire_env.env()
            action_freq = {0:0,1:0,2:0,3:0,4:0,5:0}
            
            step,won = gp.greedy_policy(env,self.max_steps_per_game,action_freq,actions_matrix,this_game,self.fp_flag,self.save_collected_data)
            
            if won == True:
                wins+=1
                 
            actions_for_each_game[this_game] = action_freq
            different_states_per_game[this_game] = len(env.hashable_map.keys())
            iterations_used_per_game[this_game] = step

        return wins,actions_matrix
    
    
    def run_all_episodes(self):
        
        
        
        for run in range(self.number_of_runs):
            
            this_run_data = {}
            wins, actions_and_states = self.run_one_episode()
            
            this_run_data['number_of_wins'] = wins
            this_run_data['actions_and_states'] = actions_and_states
            
            self.all_runs[run] = this_run_data
            
            self.win_count.append(wins)
            
            
            
            print("run {} completed".format(run+1))
        
        with open("games/hardgames_data.pkl","wb") as file:
            pkl.dump(self.save_collected_data,file)
    def average_wins_for_runs(self):
        
        win_percentage = [x*100 / self.games_per_run for x in self.win_count]
        
        
        return "avergae win percentage is {}".format(( sum(win_percentage) / self.number_of_runs))
        
    def save_runs_data(self):
        
        name = "all_runs/runs"+ str(self.number_of_runs) + str(pd.Timestamp.now()) + ".pkl"
        
        with open(name,"wb") as file:
            pkl.dump(self.all_runs,file)
            
            
        return "Data for this run saved successfully..."
    
    
if __name__ == "__main__":
    collect_data = Collect_data(N=10,games_per_run=10000)
    collect_data.run_all_episodes()
    print(collect_data.average_wins_for_runs())
    
    print(collect_data.save_runs_data())
