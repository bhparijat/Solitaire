def greedy_policy(en=None,tot=20000,action_freq={},actions_matrix=[],game=None,fp_flag=False,debug=False,save_all_states = False,save_collected_data= {},save_actions_matrix=False):
    
    actions_m = []
    
    start_state = en.copy_state()
    
    game_states = [start_state]
    
    for step in range(tot):
        
        for action in range(6):
            
            won,taken = en.step(action,fp_flag,debug)
            
             
            if won == True:
                action_freq[action]+=1
                
                actions_m.append(action)
                
                
                
                if save_actions_matrix == True:
                    game_states.append(en.state)
                    actions_matrix[game] = [game,actions_m,en.state,start_state,"won"] 
                
                hashable_state = en.generate_hashable_state_modified(en.state)
                save_collected_data[hashable_state] = action
                
                
                if save_all_states == True:
                    actions_matrix[game].append(game_states)
                    
                return len(actions_m),True
            
            if taken == True:
                action_freq[action]+=1
                
                actions_m.append(action)
                if save_actions_matrix == True:
                    game_states.append(en.state)
                
                hashable_state = en.generate_hashable_state_modified(en.state)
                save_collected_data[hashable_state] = action
                break

        if taken == False:
            
            if save_actions_matrix:
                actions_matrix[game] = [game,actions_m,en.state,start_state,"No action could be taken"] 
                
            if save_all_states == True:
                    actions_matrix[game].append(game_states)
                    
            return len(actions_m),False
        
    if save_actions_matrix:
        actions_matrix[game] = [game,actions_m,en.state,start_state,"Steps exhausted"] 
    
    if save_all_states == True:
                    actions_matrix[game].append(game_states)
    
    return len(actions_m),False
        