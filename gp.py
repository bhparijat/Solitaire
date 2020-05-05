def greedy_policy(en,tot,action_freq,actions_matrix,game,fp_flag=False,debug=False,save_all_states = False):
    
    actions_m = []
    
    start_state = en.copy_state()
    
    game_states = [start_state]
    
    for step in range(tot):
        
        for action in range(6):
            
            won,taken = en.step(action,fp_flag,debug)
            
             
            if won == True:
                action_freq[action]+=1
                
                actions_m.append(action)
                
                game_states.append(en.state)
                
                actions_matrix[game] = [game,actions_m,en.state,start_state,"won"] 
                
                if save_all_states == True:
                    actions_matrix[game].append(game_states)
                    
                return len(actions_m),True
            
            if taken == True:
                action_freq[action]+=1
                
                actions_m.append(action)
                game_states.append(en.state)
                
                break

        if taken == False:
            
            actions_matrix[game] = [game,actions_m,en.state,start_state,"No action could be taken"] 
            if save_all_states == True:
                    actions_matrix[game].append(game_states)
                    
            return len(actions_m),False
        
       
    actions_matrix[game] = [game,actions_m,en.state,start_state,"Steps exhausted"] 
    
    if save_all_states == True:
                    actions_matrix[game].append(game_states)
    
    return len(actions_m),False
        