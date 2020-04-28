def greedy_policy(en,tot,action_freq,actions_matrix,game,fp_flag=False):
    

    actions_m = []
    
    
    
    start_state = en.copy_state()
    
    
    for step in range(tot):
        
        for action in range(6):
            
            won,taken = en.step(action,fp_flag)
            
             
            if won == True:
                action_freq[action]+=1
                
                actions_m.append(action)
                
                
                actions_matrix[game] = [game,actions_m,en.state,start_state,True] 
                
                return step,True
            
            if taken == True:
                action_freq[action]+=1
                
                actions_m.append(action)
                
                break

        if taken == False:
            
            actions_matrix[game] = [game,actions_m,en.state,start_state,False] 
            
            return step,False
        
       
    actions_matrix[game] = [game,actions_m,en.state,start_state,False] 
    
    
    
    return step,False