# DOING OBJECTS WITHIN OBJECTS
# RECEIVING OBJECT THAT CONTAINS:
# map
# creature health
# player inventory

import os
#can we please figure out what this actually does? or at least someone tell me since idk
os.environ['LINES'] = '40'
os.environ['COLUMNS']= '80'

## CLASSES
class sendObject():
    # keystrokes
    def __init__(keystroke):
        self.keystroke = keystroke

#This function prints the board - do not change it
def printBoard(board):
    for row in board:
        for character in row:
            print(character, end=" ")

# placeholder for creature.printstats()
def printStats(creature):
    print(creature.object + ": " + str(creature.health) + ", " + str(creature.AIState) + ", " + str(creature.AIVector))
    print(creature.object + " inv: " + creature.inventory.weapon.name + ", " + creature.inventory.armour.name + ", " + creature.inventory.item.name)

# NEEDS REWORKING FOR THE NETWORK STUFF
def playerTurn(self,board):
    #This function decides on players actions - you could potentially add more actions in here
    action = input('What do you want to do: ')

    keys = ['w','a','s','d']

    if action in keys:
        #movement
    elif action == 'i':
        #item
    elif action == "yea boiiiiiii":
        #holla at ya boi

## NETWORKING FUNCTIONS
# sending strings
def sendStuff():
    

# receive a dictionary of strings and/or integers
def receiveStuff():
    
    
