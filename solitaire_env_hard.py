import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
import unittest
from tqdm import tqdm

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
            
            
            
            
            
                        

class env:
    
    def __init__(self):
        
        self.state = state()
        self.action_n = 6
        self.hashable_state = None
        #print("called")
        
        self.hashable_map = {}
        self.map = {}
        self.number_of_states = 0
        
        self.action_description = []
    def reset(self):
        self.state = state()
    
    def copy_state(self):
        
        new_state = state()
        
        new_state.pile = []
        
        new_state.tableau = []
        
        new_state.foundation = []
        
        
        for cd in self.state.pile:
            new_state.pile.append(card(cd.color,cd.suit,cd.number,cd.speciality,cd.face))
            
            
            
        for i in range(7):   
            
            new_state.tableau.append([])
            
            for cd in self.state.tableau[i]:
                
                
                new_state.tableau[i].append(card(cd.color,cd.suit,cd.number,cd.speciality,cd.face))
                
                
                
        for i in range(4):
            
            new_state.foundation.append([])
            
            for cd in self.state.foundation[i]:
                
            
                new_state.foundation[i].append(card(cd.color,cd.suit,cd.number,cd.speciality,cd.face))
                
                
                
                
        return new_state
    def generate_deep_copy_state(self,to_copy_state):
        
        deep_copy_state = state()
        
        deep_copy_state.pile = []
        deep_copy_state.tableau = [[] for _ in range(7)]
        deep_copy_state.foundation = [[] for _ in range(4)]
        
        for cd in to_copy_state.pile:
            new_card = card(cd.color,cd.suit,cd.number,cd.speciality,cd.face)
            deep_copy_state.pile.append(new_card)
            
            
        for i in range(7):
            
            for cd in to_copy_state.tableau[i]:
                new_card = card(cd.color,cd.suit,cd.number,cd.speciality,cd.face)

                deep_copy_state.tableau[i].append(new_card)
                
                
                
                
        for i  in range(4):
            for cd in to_copy_state.foundation[i]:
                new_card = card(cd.color,cd.suit,cd.number,cd.speciality,cd.face)

                deep_copy_state.foundation[i].append(new_card)
                
                
        
        return deep_copy_state
    
    
        
    def current_state(self):
        return self.state
    
    def get_card_tuple(self,cd):
        
        card_tuple = (cd.get_suit_number(),cd.number,cd.get_color_number(),cd.get_face_number())
        
        return card_tuple
    
    def generate_hashable_state_modified(self,state):
        
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
        
        
    def step(self,action,fp_flag,debug):
        
        taken = None
        
        
        if debug == True:
            print("Debug is True")
            
        if action == 0 :
            taken = self.tableau_to_foundation_reveal()
            
        elif action == 1:
            taken = self.to_foundation_stack(debug)
            
        elif action == 2:
            taken = self.tableau_to_tableau_reveal()
            
        elif action == 3:
            taken = self.pile_to_tableau(debug)
            
        elif action == 4:
            taken = self.foundation_to_tableau(fp_flag,debug)
            
        elif action == 5:
            taken = self.tableau_to_tableau_not_reveal(debug)
    
        
        key = self.generate_hashable_state_modified(self.state)
        
        #print(tuple(self.hashable_state))
        
        ##key = tuple(self.hashable_state)
        if key not in self.map:
            self.map[key] = 0
            
        self.map[key]+=1
        
        
        return self.isterminal(),taken
    
    
    
    def print_card(self,card,i):
        print("position {:4} suit = {:10s} color = {:10s} number = {:5} speciality = {:10s} face = {:5s}".format(i,card.suit,card.color,card.number,str(card.speciality),card.face))

    def print_cards(self,cards):
        
        for i,card in enumerate(cards):
            self.print_card(card,i)
    
    def check_compatible(self,card):
        
        f = self.suit_number(card.suit)
        
        if card.number == 1 or (len(self.state.foundation[f])> 0 and card.number == self.state.foundation[f][-1].number+1):
            return True
                
                
        return False
                
        
    def suit_number(self,suit):
        
        if suit == 'club':
            return 0
        elif suit == 'heart':
            return 1 
        elif suit == 'diamond':
            return 2
        else:
            return 3
    def highlight_movable_cards_pile(self):
        
        movable_where = []
        
        movable_indices_tableau = []
        movable_indices_foundation = []
        for i,card in enumerate(self.state.pile):
            
            movable_where.append([])

            movable_where[i] = {'tableau':[],'foundation':[]}
            
            
            #if (i%3) == 0 or len(self.state.pile)<3:
                
            if (i%3) == 0:

                for f in range(7):

                    cond1 = len(self.state.tableau[f]) == 0 and  card.number == 13

                    cond2 = len(self.state.tableau[f]) > 0 and self.state.tableau[f][-1].color != card.color and card.number+1 == self.state.tableau[f][-1].number

                    if cond1 or cond2:
                        movable_where[i]['tableau'].append(f)


                if self.check_compatible(card):
                    movable_where[i]['foundation'].append(self.suit_number(card.suit))


                if len(movable_where[i]['tableau']) !=0 :
                    movable_indices_tableau.append(i)

                if len(movable_where[i]['foundation']) != 0:
                    movable_indices_foundation.append(i)
                
        return movable_where,movable_indices_tableau,movable_indices_foundation
            
        
    def tableau_to_foundation_reveal(self):
        
        movable = []
        moves = []
        for i in range(7):
            
            movable.append([])
            
            if len(self.state.tableau[i]) <= 1 or self.state.tableau[i][-2].face == 'up': 
                continue
            
            to_move_card = self.state.tableau[i][-1]
            
            f_no = self.suit_number(to_move_card.suit)
            
            if to_move_card.number == 1:
                moves.append(i)
                
            elif len(self.state.foundation[f_no])>0 and to_move_card.number == self.state.foundation[f_no][-1].number +1:
                moves.append(i)
            
            
        
        
        if len(moves) == 0:
            return False
        
        
        
        mp = {}
        len_keys = 0
        len_moves = len(moves)
        while len_keys<len_moves:
            deep_copy_state = self.generate_deep_copy_state(self.state)
            ind = None
            while True:
                ind = random.sample(range(len_moves),1)[0]
                if ind not in mp:
                    mp[ind] = 1
                    len_keys+=1
                    break
            from_tableau = moves[ind]

            #print("tableau number ", from_tableau)

            card = deep_copy_state.tableau[from_tableau][-1]

            deep_copy_state.tableau[from_tableau].pop()

            deep_copy_state.tableau[from_tableau][-1].face = 'up'

            deep_copy_state.foundation[self.suit_number(card.suit)].append(card)
            
            hashable_state = self.generate_hashable_state_modified(deep_copy_state)
            
            if hashable_state not in self.hashable_map:
                
                self.state = deep_copy_state
                
                self.hashable_map[hashable_state] = 1
                
                
                ## adding for test environment
                
                self.state.action_description.append((from_tableau,self.suit_number(card.suit), card))
                return True
        
        return False
    def to_foundation_stack(self,debug):
        
        
        moves = []
        
        
        #print(" To foundation has been called with debug equal to ",debug)
        for i,card in enumerate(self.state.pile):
            
            
            #if (i%3)==0 or len(self.state.pile)<3:
                
            if (i%3) == 0:
                
                f_no = self.suit_number(card.suit)

                if card.number == 1 or (len(self.state.foundation[f_no]) > 0 and card.number == self.state.foundation[f_no][-1].number + 1):
                    moves.append((0,i))


        if debug == True:    
            print("moves from pile\n",moves);

               
        tableau_moves=[]

        for i in range(7):

            if len(self.state.tableau[i]) == 0:
                continue

            card = self.state.tableau[i][-1]

            f_no = self.suit_number(card.suit)

            if card.number == 1 or (len(self.state.foundation[f_no]) > 0 and card.number == self.state.foundation[f_no][-1].number + 1):
                moves.append((1,i))
                tableau_moves.append((i,card.number,card.suit,card.color))
                
          
        if len(moves) == 0:
            return False
        
        
        if debug == True:
            
            for x in tableau_moves:
                
                print("Tableau number {}, suit {}, card number {}, card color {}".format(x[0],x[2],x[1],x[3]))
        
        
        mp = {}
        len_keys = 0
        len_moves = len(moves)
        
        
        while len_keys <len_moves:
            
            
            deep_copy_state = self.generate_deep_copy_state(self.state)
            ind = None
            while True:
                ind = random.sample(range(len_moves),1)[0]
                if ind not in mp:
                    mp[ind] = 1
                    len_keys+=1
                    break
                    
                    
            #ind = random.sample(range(len(moves)),1)[0]
            
            
            
            typ, i = moves[ind]
            
            f_no = None
            card = None
            if typ == 0:

                card = deep_copy_state.pile[i]
                f_no = self.suit_number(card.suit)

                deep_copy_state.pile.pop(i)


                deep_copy_state.foundation[f_no].append(card)
            else:

                card = deep_copy_state.tableau[i][-1]

                f_no = self.suit_number(card.suit)

                deep_copy_state.tableau[i].pop()

                if len(deep_copy_state.tableau[i]) >0:

                    deep_copy_state.tableau[i][-1].face = 'up'

                deep_copy_state.foundation[f_no].append(card)

            
            hashable_state = self.generate_hashable_state_modified(deep_copy_state)
            
            if hashable_state not in self.hashable_map:
                
                self.state = deep_copy_state
                
                self.hashable_map[hashable_state] = 1
               
                ## adding action description for test environment
                
                t = "pile" if typ == 0 else "tableau"
                
                self.state.action_description((t,i,f_no,card))
                return True
            #return True
        
        return False
    def tableau_to_tableau_reveal(self):
        
        movable = []
        
        zero_len_stack = []
        for i in range(7):
            
            movable.append([])
            
            if len(self.state.tableau[i]) == 0:
                zero_len_stack.append(i)
                
            if len(self.state.tableau[i])<=1:
                continue
            
            prev = None
            for j,card in enumerate(self.state.tableau[i]):
                
                if card.face == 'up' and prev is not None and prev.face == 'down':
                    movable[i].append(j)
                    break
                    
                prev = card 
                
         
        #print("In tableu to tableu",movable)
        
        moves = []
        
        for i in range(7):
            
            for j in range(7):
                
                if i == j or len(movable[i])==0 or len(self.state.tableau[j])==0:
                    continue
                   
                
                to_move_card = self.state.tableau[i][movable[i][0]]
                
                last_card = self.state.tableau[j][-1]
                    
                
                cond1 = to_move_card.color != last_card.color
                
                cond2 = to_move_card.number + 1 == last_card.number
                
                if cond1 and cond2:
                    
                    moves.append((i,movable[i][0],j))
                    
            
            
           
        if len(zero_len_stack) > 0:
            for j in range(7):
                
                if len(movable[j]) > 0:
                    
                    cd = self.state.tableau[j][movable[j][0]]

                    if  cd.number == 13:

                        for t in zero_len_stack:

                            moves.append((j,movable[j][0],t))
            
            
                
        
        if len(moves)==0:
            return False
        
        
        
        mp = {}
        len_keys = 0
        len_moves = len(moves)
        
        while len_keys < len_moves:
            
            deep_copy_state = self.generate_deep_copy_state(self.state)
            ind = None
            
            while True:
                ind = random.sample(range(len_moves),1)[0]
                if ind not in mp:
                    mp[ind] = 1
                    len_keys+=1
                    break
        
            #ind = random.sample(range(len(moves)),1)[0]
           
            from_tableau,i,to_tableau = moves[ind]

            for card in deep_copy_state.tableau[from_tableau][i:]:

                deep_copy_state.tableau[to_tableau].append(card)



            deep_copy_state.tableau[from_tableau] = deep_copy_state.tableau[from_tableau][:i]

            deep_copy_state.tableau[from_tableau][-1].face = 'up'
            
            
            hashable_state = self.generate_hashable_state_modified(deep_copy_state)
            
            if hashable_state not in self.hashable_map:
                
                self.state = deep_copy_state
                
                self.hashable_map[hashable_state] = 1
                
                return True

            #return True
        
        return False
    def pile_to_tableau(self,debug):
        
        movable_where,movable_indices_tableau,movable_indices_foundation  = self.highlight_movable_cards_pile()
        
        if len(movable_indices_tableau) == 0:
            return False
        
        
        
        mp1,mp2 = {},{}
        len_keys = 0
        len_moves = len(movable_indices_tableau)
        
        while len_keys < len_moves:
            
            deep_copy_state = self.generate_deep_copy_state(self.state)
            ind = None
            
            while True:
                ind = random.sample(range(len_moves),1)[0]
                if ind not in mp1:
                    mp1[ind] = 1
                    len_keys+=1
                    break
        
            #ind = random.sample(range(len(movable_indices_tableau)),1)[0]



            to_move = movable_indices_tableau[ind]

            card_to_move = deep_copy_state.pile[to_move]

            
            
            tableau_index = random.sample(range(len(movable_where[to_move]['tableau'])),1)[0]

            tableau_index = movable_where[to_move]['tableau'][tableau_index]

            deep_copy_state.tableau[tableau_index].append(card_to_move)




            deep_copy_state.pile.pop(to_move)
        
            hashable_state = self.generate_hashable_state_modified(deep_copy_state)
            
            if hashable_state not in self.hashable_map:
                
                self.state = deep_copy_state
                
                self.hashable_map[hashable_state] = 1
                
                return True
            
        return True
        
    def foundation_to_tableau(self,fp_flag,debug):
        
#         moves = []
        
        if fp_flag == True:
            
            #print("flag is being checked")
            mn = 13
            mx = 0
            for i in range(4):
                if len(self.state.foundation[i]) == 0:
                    mn = 0
                    break

                mn = min(mn,self.state.foundation[i][-1].number)
                
               
            
            for i in range(4):
                
                if len(self.state.foundation[i]) == 0:
                    continue
                    
                mx = max(mx,self.state.foundation[i][-1].number)
            
            #print(mn,mx)



        if mx == 2:
            return False


        if abs(mx-mn) <=2:
            return False
        
        moves = []
        for i in range(4):
            
            if len(self.state.foundation[i]) == 0:
                continue
                
            card = self.state.foundation[i][-1]
            
            for j in range(7):
                
                if len(self.state.tableau[j]) == 0:
                    continue
                    
                
                last_card = self.state.tableau[j][-1]
                
                if last_card.color != card.color and last_card.number == card.number+1:
                    moves.append((i,j))
        
            if card.number == 13 :
                
                for j in range(7):
                    
                    if len(self.state.tableau[j]) == 0:
                        moves.append((i,j))
                        
        
        if debug == True:
            print(moves)
        
        if len(moves) == 0:
            return False
        
        mp = {}
        len_keys = 0
        len_moves = len(moves)
        
        while len_keys < len_moves:
            
            deep_copy_state = self.generate_deep_copy_state(self.state)
            #print(len(self.state.foundation[foundation]),len(deep_copy_state.foundation[foundation]))

            ind = None
            
            while True:
                ind = random.sample(range(len_moves),1)[0]
                if ind not in mp:
                    mp[ind] = 1
                    len_keys+=1
                    break
                    
            #ind = random.sample(range(len(moves)),1)[0]

            foundation,tableau = moves[ind]
            
            #print(foundation,tableau)
            #print(len(self.state.foundation[foundation]),len(deep_copy_state.foundation[foundation]))
            card = deep_copy_state.foundation[foundation][-1]

            deep_copy_state.foundation[foundation].pop()

            deep_copy_state.tableau[tableau].append(card)



            hashable_state = self.generate_hashable_state_modified(deep_copy_state)

            if hashable_state not in self.hashable_map:

                self.state = deep_copy_state

                self.hashable_map[hashable_state] = 1

                return True
        
        return False
    def tableau_to_tableau_not_reveal(self,debug):
        
        
        movable = []
        
        for i in range(7):
            
            first = False
            movable.append([])
            for j,card in enumerate(self.state.tableau[i]):
                
                if card.face == 'up' and j == 0:
                    
                    movable[i].extend(range(len(self.state.tableau[i])))
                    
                    break
                elif card.face == 'up' and first == True:
                    
                    movable[i].append(j)
                
                elif card.face == 'up':
                    first = True
                    
        #to_move = []
        
        if debug == True:
            
            for i in range(7):
                
                print("cards movable in tableau {} \n".format(i),movable[i])
                
                
                
        where_to_move = []
        
        which_movable_tableaus = []
        
        
        for i in range(7):
            
            #to_move.append([])
            where_to_move.append([])
            for j,to_move in enumerate(movable[i]):
            
                for k in range(7):

                    if i == k:
                        continue

                    to_move_card = self.state.tableau[i][to_move]



                    condition1 = len(self.state.tableau[k])>0 and to_move_card.color != self.state.tableau[k][-1].color  
                    condition2 = len(self.state.tableau[k])>0 and to_move_card.number+1 == self.state.tableau[k][-1].number

                    if debug == True:
                        print(condition1,condition2)
                    if condition1==True and condition2==True:
                        where_to_move[i].append(j)

                        which_movable_tableaus.append((i,j,k))
                    else:

                        where_to_move[i].append(np.inf)
                            
                 
        if debug == True:
            
            print(len(which_movable_tableaus))
            for i,j,k in which_movable_tableaus:
                print(" from tableau {} to tableau {}, card {}".format(i,k,j))
                
        
        if len(which_movable_tableaus) == 0:
            return False
        
        
        
                
                
                
        mp = {}
        len_keys = 0
        len_moves = len(which_movable_tableaus)
        
        while len_keys < len_moves:
            
            deep_copy_state = self.generate_deep_copy_state(self.state)
            ind = None
            
            while True:
                ind = random.sample(range(len_moves),1)[0]
                if ind not in mp:
                    mp[ind] = 1
                    len_keys+=1
                    break
                    
                    
            #ind = random.sample(range(len(which_movable_tableaus)),1)[0]

            from_tableau, cards_to_move,to_tableau = which_movable_tableaus[ind]





            for cd in deep_copy_state.tableau[from_tableau][cards_to_move:]:

                deep_copy_state.tableau[to_tableau].append(cd)


            deep_copy_state.tableau[from_tableau] = deep_copy_state.tableau[from_tableau][:cards_to_move]


            hashable_state = self.generate_hashable_state_modified(deep_copy_state)

            if hashable_state not in self.hashable_map:

                self.state = deep_copy_state

                self.hashable_map[hashable_state] = 1

                return True
        
        return False
        
    def get_pile(self):
        
        self.print_cards(self.state.pile)
        
    def get_tableau(self):
        
        for i,tableau in enumerate(self.state.tableau):
            print("printing tableau number {} ********************".format(i+1))
            self.print_cards(tableau)
            
    def get_foundation(self):
        
        for i,foundation in enumerate(self.state.foundation):
            print("printing foundation number {} ********************".format(i+1))
            self.print_cards(foundation)
        
            
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
        
    