class card:
    """
    Defines structure for a card
    
    """
    def __init__(self,color,suit,number,speciality,face):
        """
        Args:
            color ==> red or black
            suit ===> club, heart, diamond, spade
            number ==> 1 to 13
            speciality ==> None or Ace, King, Queen,Jack
        """
        self.suit = suit
        self.color = color
        self.number = number
        self.speciality = speciality
        self.face = face
       
    def get_suit_number(self):
        
        suit_map = {"club":0,"heart":1,"diamond":2,"spade":3}
        
        return suit_map[self.suit]
    
    def get_color_number(self):
        
        color_map = {"red":0,"black":1}
        
        return color_map[self.color]
    
    def get_face_number(self):
        
        face_map = {"up":0,"down":1}
        
        return face_map[self.face]
    
    
    
class TestEnv:
    
    def __init__(self,state):
        
        self.start_state = state
        self.state = state
        self.hashable_map = {}
        
        
    def reset(self):
        
        self.state = self.start_state
        self.hashable_map = {}
        
        
    def step(self,action,debug,action_data):
        
        if action == 0:
            taken = self.tableau_to_foundation_reveal(debug,action_data)
            
        elif action == 1:
            taken = self.to_foundation_stack(debug,action_data)
            
        elif action == 2:
            taken = self.tableau_to_tableau_reveal(debug,action_data)
        elif action == 3:
            taken = self.pile_to_tableau(debug,action_data)
        elif action == 4:
            taken =  self.foundation_to_tableau(debug,action_data)
        else:
            taken = self.tableau_to_tableau_not_reveal(debug,action_data)
            
            
        return self.isterminal(),taken
     
    def get_card_tuple(self,cd):
        
        card_tuple = (cd.get_suit_number(),cd.number,cd.get_color_number(),cd.get_face_number())
        
        return card_tuple
     
    
    def get_foundation(self):
        
        for i in range(4):
            for j,cd in enumerate(self.foundation[i]):
                print("position={} suit={} color={} number={} face={}".format(j,cd.suit,cd.color,cd.number,cd.face))
    
    def get_pile(self):
        
        for j,cd in enumerate(self.pile):
            print("position={} suit={} color={} number={} face={}".format(j,cd.suit,cd.color,cd.number,cd.face))

    def get_tableau(self):
        
        for i in range(7):
            for j,cd in enumerate(self.tableau[i]):
                print("position={} suit={} color={} number={} face={}".format(j,cd.suit,cd.color,cd.number,cd.face))
                
                

    def get_hashable_state(self):
        hashable_state = []
        
        hashable_state_pile = []
        
        for cd in state.pile:
            card_tuple = self.get_card_tuple(cd)
            hashable_state_pile.append(card_tuple)
        
        tableau_hashed = []
        
        for i in range(7):
            
            hashable_state_tableau = []
            
            for cd in state.tableau[i]:

                card_tuple = self.get_card_tuple(cd)
                hashable_state_tableau.append(card_tuple)
                
            
            tableau_hashed.append(tuple(hashable_state_tableau))
            
          
        foundation_hashed = []
        
        for i in range(4):
            
            
            hashable_state_foundation = []
            for cd in state.foundation[i]:
                
                
                card_tuple = self.get_card_tuple(cd)
                hashable_state_foundation.append(card_tuple)
                
            foundation_hashed.append(tuple(hashable_state_foundation))
            
            
            
        hashable_state = [tuple(hashable_state_pile), tuple(foundation_hashed), tuple(tableau_hashed) ]
        
        
        return tuple(hashable_state)
    def tableau_to_foundation_reveal(self,debug,action_data):
        
        from_tableau,to_foundation,moved_card = action_data
        
        cd = self.state.tableau[from_tableau].pop()
        
        if debug == True:
            self.compare_cards(cd,moved_card)
            
        self.state.foundation[to_foundation].append(cd)
        
        hashable_state = self.get_hashable_state()
        
        if hashable_state in self.hashable_map:
            return False
        
        self.hashable_map[hashable_state] = 1
        return True
       
        
    def to_foundation_stack(self,debug,action_data):
        
        typ, from_position,to_foundation, moved_card = action_data
        
        if typ == "pile":
            
            cd = self.state.pile.pop(from_position)
            
        else:
            
            cd = self.state.tableau[from_position].pop()
            
            
        if debug == True:
            print(self.compare_cards(cd,moved_card))


        self.foundation[to_foundation].append(cd)

        hashable_state = self.get_hashable_state()

        if hashable_state in self.hashable_map:
            return False

        self.hashable_map[hashable_state] = 1

        return True
        
            
            
    def tableau_to_tableau_reveal(self,debug,action_data):
        
        from_tableau, to_tableau, from_tableau_position, moved_card_stack = action_data
            
        cd_stack = self.state.tableau[from_tableau][from_tableau_position:]
        
        if debug == True:
            
            match = True
            
            for cd1,cd2 in zip(cd_stack,moved_card):
                match = match and self.compare_cards(cd1,cd2)
                
                
        
        self.state.tableau[from_tableau] =  self.state.tableau[from_tableau][:from_tableau_position]
        
        
        self.state.tableau[from_tableau][-1].face = 'up'
        
        for cd in cd_stack:
            
            self.state.tableau[to_tableau].append(cd)
            
            
            
        hashable_state = self.get_hashable_state()

        if hashable_state in self.hashable_map:
            return False

        self.hashable_map[hashable_state] = 1

        return True
            
            
    def pile_to_tableau(self,debug,action_data):        
            
            
        from_pile_position, to_tableau, moved_card = action_data
        
        cd = self.state.pile.pop(from_pile_position)
        
        if debug == True:
            print(self.compare_card(cd,moved_card))
            
            
        self.state.tableau[to_tableau].append(cd)   
            
        hashable_state = self.get_hashable_state()

        if hashable_state in self.hashable_map:
            return False

        self.hashable_map[hashable_state] = 1

        return True
            
            
            
            
    def foundation_to_tableau(self, debug,action_data):
        
            
        from_foundation, to_tableau, moved_card = action_data
                
        cd = self.state.foundation.pop()
        
        if debug == True:
            print(self.compare_card(cd,moved_card))
            
        self.state.tableau[to_tableau].append(cd)
        
        if hashable_state in self.hashable_map:
            return False

        self.hashable_map[hashable_state] = 1

        return True
            
        
    def tableau_to_tableau_not_reveal(self,debug,action_data):
        
        from_tableau, to_tableau, from_tableau_position, moved_card_stack = action_data
        
        cd_stack = self.state.tableau[from_tableau][from_tableau_position:]
        
        if debug == True:
            
            match = True
            
            for cd1,cd2 in zip(cd_stack,moved_card):
                match = match and self.compare_cards(cd1,cd2)
                
            print(match)
                
        
        self.state.tableau[from_tableau] =  self.state.tableau[from_tableau][:from_tableau_position]
        
        
        
        
        for cd in cd_stack:
            
            self.state.tableau[to_tableau].append(cd)
            
            
            
        hashable_state = self.get_hashable_state()

        if hashable_state in self.hashable_map:
            return False

        self.hashable_map[hashable_state] = 1

        return True
            