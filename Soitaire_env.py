

import numpy as np
import matplotlib.pyplot as plt
import random
import time
import unittest




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
        
        pile_index = self.make_pile()
        _ = self.make_tableau(pile_index)
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
            self.tableau[i][-1].face = 'up'
            
        check1.sort()
        check2.sort()
        
        #print(check1)
        #print(check2)
        
        assert check1 == check2
        #print(a)
                
    def gen_special_cards(self,color,suit,face = 'down'):
        
        self.all_cards.append(card(color,suit,1,'ACE',face))
        self.all_cards.append(card(color,suit,11,'KING',face))
        self.all_cards.append(card(color,suit,12,'QUEEN',face))
        self.all_cards.append(card(color,suit,13,'JACK',face))
        
        
    def gen_non_special_cards(self,color,suit,face = "down",speciality = None):
        
        for number in range(2,11):
            self.all_cards.append(card(color,suit,number,speciality,face))



class env:
    
    def __init__(self):
        
        self.state = state()
        self.action_n = 6
    def reset(self):
        self.state = state()
        
    def current_state(self):
        return self.state
    
    def step(self,action):
        
        taken = None
        if action == 0 :
            taken = self.tableau_to_foundation_reveal()
            
        elif action == 1:
            taken = self.to_foundation_stack()
            
        elif action == 2:
            taken = self.tableau_to_tableau_reveal()
            
        elif action == 3:
            taken = self.pile_to_tableau()
            
        elif action == 4:
            taken = self.foundation_to_tableau()
            
        elif action == 5:
            taken = self.tableau_to_tableau_not_reveal()
    
    
        return self.state, self.isterminal(),taken
    
    def print_card(self,card):
        print("suit = {:10s} color = {:10s} number = {:5} speciality = {:10s} face = {:5s}".format(card.suit,card.color,card.number,str(card.speciality),card.face))

    def print_cards(self,cards):
        
        for card in cards:
            self.print_card(card)
    
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
        
        ind = random.sample(range(len(moves)),1)[0]
                
        from_tableau = moves[ind]
        
        #print("tableau number ", from_tableau)
        
        card = self.state.tableau[from_tableau][-1]
        
        self.state.tableau[from_tableau].pop()
        
        self.state.tableau[from_tableau][-1].face = 'up'
        
        self.state.foundation[self.suit_number(card.suit)].append(card)
        
        return True
    def to_foundation_stack(self):
        
        
        moves = []
        
        
        for i,card in enumerate(self.state.pile):
            
            f_no = self.suit_number(card.suit)
            
            if card.number == 1 or (len(self.state.foundation[f_no]) > 0 and card.number == self.state.foundation[f_no][-1].number + 1):
                moves.append((0,i))
                
            
            
        
        for i in range(7):
            
            if len(self.state.tableau[i]) == 0:
                continue
                
            card = self.state.tableau[i][-1]
            
            f_no = self.suit_number(card.suit)
            
            if card.number == 1 or (len(self.state.foundation[f_no]) > 0 and card.number == self.state.foundation[f_no][-1].number + 1):
                moves.append((1,i))
                
                
          
        if len(moves) == 0:
            return False
        
        
        ind = random.sample(range(len(moves)),1)[0]
        
        typ, i = moves[ind]
        
        if typ == 0:
            
            card = self.state.pile[i]
            f_no = self.suit_number(card.suit)
            
            self.state.pile.pop(i)
            
            
            self.state.foundation[f_no].append(card)
        else:
            
            card = self.state.tableau[i][-1]
            
            f_no = self.suit_number(card.suit)
            
            self.state.tableau[i].pop()
            
            if len(self.state.tableau[i]) >0:
                
                self.state.tableau[i][-1].face = 'up'
                
            self.state.foundation[f_no].append(card)
            
            
        
        return True
    def tableau_to_tableau_reveal(self):
        
        movable = []
        
        for i in range(7):
            
            movable.append([])
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
                    
                    
        
        if len(moves)==0:
            return False
        
        ind = random.sample(range(len(moves)),1)[0]
           
        from_tableau,i,to_tableau = moves[ind]
        
        for card in self.state.tableau[from_tableau][i:]:
            
            self.state.tableau[to_tableau].append(card)
            
            
        
        self.state.tableau[from_tableau] = self.state.tableau[from_tableau][:i]
          
        self.state.tableau[from_tableau][-1].face = 'up'
            
        
        return True
    def pile_to_tableau(self):
        
        movable_where,movable_indices_tableau,movable_indices_foundation  = self.highlight_movable_cards_pile()
        
        if len(movable_indices_tableau) == 0:
            return False
        
        move_index = random.sample(range(len(movable_indices_tableau)),1)
        
        move_index = move_index[0]
        
        to_move = movable_indices_tableau[move_index]
        
        card_to_move = self.state.pile[to_move]
        
        
        tableau_index = random.sample(range(len(movable_where[to_move]['tableau'])),1)[0]
        
        tableau_index = movable_where[to_move]['tableau'][tableau_index]
        
        self.state.tableau[tableau_index].append(card_to_move)
        
        
        #print("card to move is *********")
        #self.print_card(card_to_move)
        check1 = len(self.state.pile)
        #print("State pile before card is moved******")
        #self.print_cards(self.state.pile)
        
        
        self.state.pile =  [card for card in self.state.pile if card is not card_to_move]
        
        #print("state pile after card if moved********")
        #self.print_cards(self.state.pile)
        
        check2 = len(self.state.pile)
        
        assert check1==check2+1
        
        return True
        
    def foundation_to_tableau(self):
        
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
        
        
        
        if len(moves) == 0:
            return False
        
        
        ind = random.sample(range(len(moves)),1)[0]
        
        foundation,tableau = moves[ind]
        
        card = self.state.foundation[foundation][-1]
        
        self.state.foundation[foundation].pop()
        
        self.state.tableau[tableau].append(card)
        
        return True
    def tableau_to_tableau_not_reveal(self):
        
        
        movable = []
        
        for i in range(7):
            
            first = False
            movable.append([])
            for j,card in enumerate(self.state.tableau[i]):
                
                if card.face == 'up' and i == 0:
                    
                    movable[i].extend(range(len(self.state.tableau[i])))
                    
                    break
                elif card.face == 'up' and first == True:
                    
                    movable[i].append(j)
                
                elif card.face == 'up':
                    first = True
                    
        #to_move = []
        
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
                        
                        if condition1 and condition2:
                            where_to_move[i].append(j)
                            
                            which_movable_tableaus.append((i,j,k))
                        else:
                            
                            where_to_move[i].append(np.inf)
                            
                 
        
        if len(which_movable_tableaus) == 0:
            return False
        
        move = random.sample(range(len(which_movable_tableaus)),1)
        
        from_tableau, cards_to_move,to_tableau = which_movable_tableau[move[0]]
        
        
        #print("From move tableau Before *********")
        
        #self.print_cards(self.state.tableau[from_tableau])
        
        #print("To move tableau Before *********")
        
        
        #self.print_cards(self.state.tableau[to_tableau])
        
        
        for card in self.state.tableau[from_tableau[cards_to_move:]]:
            
            self.state.tableau[to_tableau].append(card)
             
        
        self.state.tableau[from_tableau] = self.state.tableau[from_tableau[:cards_to_move]]
            
        
        #print("From move tableau after move")
        
        #self.print_cards(self.state.tableau[from_tableau])
        
        #print("To move tableau Before *********")
        
        #self.print_cards(self.state.tableau[to_tableau])
        
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
        
        for i in range(len(self.state.tableau)):
            ans = ans and (len(self.state.tableau[i]) == 0 )
            
            
        
        
        for i in range(len(self.state.foundation)):
            ans = ans and (len(self.state.foundation)==13)
            
            
            
        return ans   
        
    



import time
start = time.time()


count = 0
for j in range(100):
    en = env()
    for i in range(1000000):

        action = random.sample(range(6),1)[0]


        _,won,_ = en.step(action)

        #print(i+1,action,won)
        if won == True:
            count+=1
            break
        

print(count/10)
print(time.time()-start)





print(en.get_pile())





print(en.get_foundation())





print(en.get_tableau())

