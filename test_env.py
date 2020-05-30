import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import time

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
    
class state:
    """
    Defines the structure of a state. A state holds pile, foundation and tableau, cards to review. 
    
    """
    def __init__(self):
        
        """
        A state comprises of :
            4 foundations ==> club, heart, diamond, spade in that order
        
            7 tableaus ===> cards facing up or down
            
            1 pile ===> empty or has cards
        
        """
        
        self.all_cards = []
        self.pile = None
        self.tableau = [[] for i in range(7)]
        self.foundation = [[],[],[],[]]
        
        self.gen_non_special_cards('red','heart')
        self.gen_non_special_cards('red','diamond')
        self.gen_non_special_cards('black','spade')
        self.gen_non_special_cards('black','club')
        
        
        self.gen_special_cards('red','heart')
        self.gen_special_cards('red','diamond')
        self.gen_special_cards('black','spade')
        self.gen_special_cards('black','club')
        
        #print(len(self.all_cards))
        
        random.shuffle(self.all_cards)
        
        pile_index = self.make_pile()
        _ = self.make_tableau(pile_index)
        
        self.hashable_state = None
    def make_pile(self):
        
        pile_index = random.sample(range(len(self.all_cards)),24 )
        
        pile_index.sort()
        self.pile = [self.all_cards[i] for i in pile_index]
        
        for card in self.pile:
            card.face = 'up'
        #print(self.pile)
        
        return pile_index
    
   
            
    def make_tableau(self,pile_index):
        
        #print(pile_index)
        tableau_index = [i for i in range(len(self.all_cards)) if i not in pile_index]
        check1 = tableau_index[:]
        check2 = []
        #print("index of cards to be in tableau ", tableau_index)
        
        for i in range(1,8):
            
            all_cards_this_tableau_index = random.sample(range(len(tableau_index)),i)
            
            all_cards_this_tableau = [tableau_index[x] for x in all_cards_this_tableau_index]
            #print("index of cards to be in {} tableau".format(i),all_cards_this_tableau)
            
            tableau_index = [x for x in tableau_index if x not in all_cards_this_tableau]
            
            for card_index  in all_cards_this_tableau:
                
                
                self.tableau[i-1].append(self.all_cards[card_index])
                check2.append(card_index)
        
        
        for i in range(7):
            for cd in self.tableau[i]:
                cd.face = 'down'
        
        for i in range(7):
            self.tableau[i][-1].face = 'up'
          
        
        check1.sort()
        check2.sort()
        
        #print(check1)
        #print(check2)
        
        assert check1 == check2
        #print(a)
                
    def gen_special_cards(self,color,suit,face = 'down'):
        
        self.all_cards.append(card(color,suit,1,'ACE',face))
        self.all_cards.append(card(color,suit,13,'KING',face))
        self.all_cards.append(card(color,suit,12,'QUEEN',face))
        self.all_cards.append(card(color,suit,11,'JACK',face))
        
        
    def gen_non_special_cards(self,color,suit,face = "down",speciality = None):
        
        for number in range(2,11):
            self.all_cards.append(card(color,suit,number,speciality,face))
            
            
    
class TestEnv:
    
    def __init__(self,start_state):
        
        self.start_state = start_state
        self.state = state()
        
        self.make_state(start_state)
        
        self.hashable_map = {}
        
    def make_state(self,state):
        
        self.state.pile = []
        self.state.tableau = []
        self.state.foundation = []
        
        
        for cd in state.pile:
            self.state.pile.append(card(cd.color,cd.suit,cd.number,cd.speciality,cd.face))
            
            
        for i in range(7):
            
            self.state.tableau.append([])
            
            for cd in state.tableau[i]:
                
                self.state.tableau[i].append(card(cd.color,cd.suit,cd.number,cd.speciality,cd.face))
                
                
        for i in range(4):
            self.state.foundation.append([])
            
            for cd in state.foundation[i]:
                self.state.foundation[i].append(card(cd.color,cd.suit,cd.number,cd.speciality,cd.face))
    def reset(self):
        
        self.state = self.start_state
        self.hashable_map = {}
        
        
    def step(self,action=0,debug=True,action_data=(0,0,None)):
        
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
        
           for i,foundation in enumerate(self.state.foundation):
                print("printing foundation number {} ********************".format(i+1))
                self.print_cards(foundation)
     
    def print_card(self,card,i):
        print("position {:4} suit = {:10s} color = {:10s} number = {:5} speciality = {:10s} face = {:5s}".format(i,card.suit,card.color,card.number,str(card.speciality),card.face))
    def print_cards(self,cards):
        
        for i,card in enumerate(cards):
            self.print_card(card,i)
            
    def get_pile(self):
        
        self.print_cards(self.state.pile)
        
    def get_tableau(self):
        
        for i,tableau in enumerate(self.state.tableau):
            print("printing tableau number {} ********************".format(i+1))
            self.print_cards(tableau)
                

    def get_hashable_state(self):
        hashable_state = []
        
        hashable_state_pile = []
        
        for cd in self.state.pile:
            card_tuple = self.get_card_tuple(cd)
            hashable_state_pile.append(card_tuple)
        
        tableau_hashed = []
        
        for i in range(7):
            
            hashable_state_tableau = []
            
            for cd in self.state.tableau[i]:

                card_tuple = self.get_card_tuple(cd)
                hashable_state_tableau.append(card_tuple)
                
            
            tableau_hashed.append(tuple(hashable_state_tableau))
            
          
        foundation_hashed = []
        
        for i in range(4):
            
            
            hashable_state_foundation = []
            for cd in self.state.foundation[i]:
                
                
                card_tuple = self.get_card_tuple(cd)
                hashable_state_foundation.append(card_tuple)
                
            foundation_hashed.append(tuple(hashable_state_foundation))
            
            
            
        hashable_state = [tuple(hashable_state_pile), tuple(foundation_hashed), tuple(tableau_hashed) ]
        
        
        return tuple(hashable_state)
    def tableau_to_foundation_reveal(self,debug,action_data):
        
        action_number,from_tableau,to_foundation,moved_card = action_data
        
        cd = self.state.tableau[from_tableau].pop()
        
        self.state.tableau[from_tableau][-1].face = 'up'
        
        if debug == True:
            self.compare_cards(cd,moved_card)
            
        self.state.foundation[to_foundation].append(cd)
        
        hashable_state = self.get_hashable_state()
        
        if hashable_state in self.hashable_map:
            return False
        
        self.hashable_map[hashable_state] = 1
        return True
       
        
    def to_foundation_stack(self,debug,action_data):
        
        action_number,typ, from_position,to_foundation, moved_card = action_data
        
        if typ == "pile":
            
            cd = self.state.pile.pop(from_position)
            
        else:
            
            cd = self.state.tableau[from_position].pop()
            
            
        if debug == True:
            print(self.compare_cards(cd,moved_card))


        self.state.foundation[to_foundation].append(cd)

        hashable_state = self.get_hashable_state()

        if hashable_state in self.hashable_map:
            return False

        self.hashable_map[hashable_state] = 1

        return True
        
            
            
    def tableau_to_tableau_reveal(self,debug,action_data):
        
        action_number,from_tableau, to_tableau, from_tableau_position, moved_card_stack = action_data
            
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
            
            
        action_number,from_pile_position, to_tableau, moved_card = action_data
        
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
        
            
        action_number,from_foundation, to_tableau, moved_card = action_data
                
        cd = self.state.foundation[from_foundation].pop()
        
        if debug == True:
            print(self.compare_card(cd,moved_card))
            
        self.state.tableau[to_tableau].append(cd)
        
        hashable_state = self.get_hashable_state()
        if hashable_state in self.hashable_map:
            return False

        self.hashable_map[hashable_state] = 1

        return True
            
        
    def tableau_to_tableau_not_reveal(self,debug,action_data):
        
        action_number,from_tableau, to_tableau, from_tableau_position, moved_card_stack = action_data
        
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
            
        
    def isterminal(self):
        
        ans = (len(self.state.pile) == 0)
        
        #print(ans)
        for i in range(len(self.state.tableau)):
            ans = ans and (len(self.state.tableau[i]) == 0 )
            
            
        #print(ans)
        
        for i in range(len(self.state.foundation)):
            ans = ans and (len(self.state.foundation[i])==13)
            
            
        #print(ans)   
        return ans   