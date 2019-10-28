


import random
import math
import pdb
from itertools import chain
import copy
import time
import sys, os
global str


possible_actions = []
class game:
  def __init__(self):
      self.tempp = 0
      self.cards = []     # NOT USED, REMOVE
      self.tcards = []    # NOT USED PRESENTLY, JUST HOLDS A COPY OF EVERYTHING
      self.stock = []                             # Contains the decked to be flipped
      self.foundation = [[],[],[],[]]
      self.talon = []                            # Contains flipped cards
      self.tableau = [[],[],[],[],[],[],[]]       # 7 cards laid out aside eachother
      # self.shuffle()
      self.score = 0
      self.stock_resets = 0      # Will be used for the three talon move game (Hard mode on Google)
      self.last_action = None    # Nor used
      self.cached_actions = []   # should be updated by an outside simulator
      self.length = len(self.stock) + len(self.talon)+len(self.tableau[0])+len(self.tableau[1])+len(self.tableau[2])+len(self.tableau[3])+len(self.tableau[4])+len(self.tableau[5])+len(self.tableau[6])+len(self.foundation[0])+len(self.foundation[1])+len(self.foundation[2])+len(self.foundation[3])
      # self.memoize = []
      self.actions = []      # All the actions taken so far, Not Recommended as Monte Carlo Tree grows very big
      self.second_last_action = None    # Is used for checking the second last card moved to prevent loops caused by repeating actions
      self.past_actions = []    # Debugging purposes
      self.open_talon = []
      self.return_game_state = 0

  def shuffle(self):
    n = []
    for i in range(1,11):
      n.append(['D','R',i,0,0,0])  # First 0 for stopping rewarding points for the same card being oscillated again, second 0 for stating whether a card is known or not
      n.append(['H','R',i,0,0,0])  #third 0 for showing that multiple cards are face up together
      n.append(['S','B',i,0,0,0])
      n.append(['C','B',i,0,0,0])

    # face_cards = ["K","Q","K","A"]
    for i in range(11,14):
      n.append(['C','B',i,0,0,0])  #third 0 for showing that multiple cards are face up together
      # n.append(['C','B',""+face_cards[i-10]])   1 - A, 11 - J, 12 - Q, 13 - K
      n.append(['S','B',i,0,0,0])
      n.append(['D','R',i,0,0,0])
      n.append(['H','R',i,0,0,0])

    #for i in range(1,26):
    self.cards = n
    self.tcards = n
    self.assign_tableau(n)
    self.create_stock()
    self.playable_stock()

    #insert code

  def get_length(self):
    self.length = len(self.stock) + len(self.talon)+len(self.tableau[0])+len(self.tableau[1])+len(self.tableau[2])+len(self.tableau[3])+len(self.tableau[4])+len(self.tableau[5])+len(self.tableau[6])+len(self.foundation[0])+len(self.foundation[1])+len(self.foundation[2])+len(self.foundation[3])
    print(self.length)


  #########################################################################################################
  # Name: assign_tableau
  # Use: Used for filling up the tableau
  # Paramterers: the list with all card combinations
  #########################################################################################################
  def assign_tableau(self,n):
    tableau_num = 0
    self.tempp += 1
    self.foundation = [[],[],[],[]]
    self.tableau = [[],[],[],[],[],[],[]]       # 7 cards laid out aside eachother
    for i in range(0,28):      # For each tableau
      # time.sleep(1)
      x = random.randint(0,len(n)-1)   # Contains the card number
      # print("x is " + str(x) + " len of x  is " + str(len(n)) + "\n")
      card = n[x]                    # Stores a copy of the card
      if(len(self.tableau[tableau_num]) < tableau_num+1):
        self.tableau[tableau_num].append(card)
        if(len(self.tableau[tableau_num]) == tableau_num+1):
          tableau_num += 1

      n.pop(x)
    for i in range(7):
      self.tableau[i][-1][4] = 1    # Makes the last card a face up card

    self.cards = n


  def create_stock(self):
    self.stock = []
    for i in range(0,24):
      #pdb.set_trace()
      x = random.randint(0,len(self.cards)-1)
      self.stock.append(self.cards[x])
      self.cards.pop(x)

  # This function eliminates the need for the stock
  def playable_stock(self):
    self.open_talon = []
    for i in range(len(self.stock)):
      if i%3 == 0:
        self.open_talon.append(self.stock[i])
        
  def flip_stock(self):
    if(len(self.stock)>=1):
      self.talon.append(self.stock.pop())
      return (0)

    elif(len(self.stock) == 0):
      self.stock_resets += 1;
      for i in range(len(self.talon)):
        self.stock.append(self.talon.pop())
        # pdb.set_trace()
      if (self.stock_resets >= 3):
        self.stock_resets = 0
        return(self.return_scoring(3))
      else:
        return(0)



if __name__ == "__main__":

	x = game()




	x.shuffle()



	print(x.open_talon)    # Is essentially the cards you can currenyly move to the tableau and foundation from the talon


	


	print(x.tableau)


	


	print(x.foundation)   #Empty in the beginn

