import random
import threading
import os
from socket import *
import pickle
from io import BytesIO

SIZE = 1024

# ALL THE CLASSES
# TEST CLASS
class AbsoluteG():
    def __init__(self):
        self.a = "aaaaaa"
        self.ga = "gaaaaaa"
        self.r = "rerererererepiratererere"

# NETWORKING CLASSES
class client(threading.Thread):
    def __init__(self,soc):
        threading.Thread.__init__(self)
        self.soc = soc
        self.RunningState = True

    def iReceive(self):
        data = self.soc.recv(SIZE)
        return data

    def run(self):
        while self.RunningState:
            msg = self.iReceive()
            print('Receive-> ',msg.decode())

# placeholder for sending information
class sendObject():
    # keystrokes
    def __init__(keystroke):
        self.keystroke = keystroke

# ITEM CLASSES
# DAMAGE : The damage multiplier the item has
# REDUCTION : The damage reduction the item has
# HEAL : The amount the item heals the user by
# NAME : The name given to the item
# DESCRIPTION : Information about the item
# USES : The number of uses the item can be used for
# RARITY : The likelyhood of a creature being given this item 
class Weapon():
    def __init__(self,damage,name,description,rarity):
        self.damage = damage
        self.name = name
        self.description = description
        self.rarity = rarity

class Armour():
    def __init__(self,reduction,name,description,rarity):
        self.reduction = reduction
        self.name = name
        self.description = description
        self.rarity = rarity

class Item():
    def __init__(self,heal,damage,reduction,name,description,uses,rarity):
        self.heal = heal
        self.damage = damage
        self.reduction = reduction
        self.name = name
        self.description = description
        self.uses = uses
        self.rarity = rarity

# INVENTORY CLASS
# class for the creature's inventory
class Inventory():
    # Weapon : the damage, name and other values for the weapon
    # Armour : same
    # FOR AN ITEM : name, value, others
    def __init__(self,weapon,armour,item):
        self.weapon = weapon
        self.armour = armour
        self.item = item

    # swaps in better items from the other given inventory
    def swapItems(self,otherInv,parent):
        if parent.player == True:
            if otherInv.weapon.damage > self.weapon.damage:
                self.weapon = otherInv.weapon
            if otherInv.armour.reduction > self.armour.reduction:
                self.armour = otherInv.armour

            if otherInv.item != iNone:
                print("You can take the item : " + otherInv.item.name)
                take = input("Do you want to take this item? [y/n]: ").lower()
                if take == "y":
                    self.item = otherInv.item

# CREATURE CLASS

# // WILL NEED WORK CHANGING THE MOVEMENT FUNCTIONS // #
# p.s. Harambe was just a gorilla

# The creature class will contain the variables required for both monsters and the player
class Creature():
    # object : character - the character that represents the creature on the board
    # player : boolean - dictates whether the creature is controlled by AI or the player
    # health : int - how much damage the creature can take before dieing
    # damageReductor : the scalar that reduces incoming damage
    # damage : int  - how much damage the creature can deal in one move
    # movements : 2D-Array - the different movements that a creature can make, as vectors in the array
    # inventory : inventory for the creature, can carry weapons, armour
    def __init__(self,object,player,health,dmgReductor,damage,movements,inventory):
        self.object = object
        self.player = player
        self.health = health
        self.damageReductor = dmgReductor
        self.damage = damage
        self.movements = movements
        self.inventory = inventory
        
        self.AIState = 0
        self.AIVector = [0,0]

    def move(self,board,aBoard):
        if self.object == "X":
            return board
        elif self.player == True:
            return self.playerTurn(board)
        else:
            return self.monstersTurn(board,aBoard)

    def playerTurn(self,board):
        #This function decides on players actions - you could potentially add more actions in here
        action = input('What do you want to do: ')

        keys = ['w','a','s','d']

        if action in keys:
            board = self.moveCreature(board,self.movements[keys.index(action)])
        elif action == 'i':
            self.useItem()
        elif action == "yea boiiiiiii":
            self.inventory.weapon = wSmax
        return board

    # The function that returns which direction the creature willtravel in
    def AI(self,board,aBoard):
        currentPosition = getObjectPosition(board,self.object)
        currentAIPositionObject = checkSquare(aBoard,currentPosition)

        if currentAIPositionObject in ["u","l","d","r"]:
            self.AIState = 1

        if self.AIState == 1:
            if currentAIPositionObject in ["u","l","d","r"]:
                aiDirector = self.movements[["u","l","d","r"].index(currentAIPositionObject)]
                self.AIVector = [self.AIVector[0] + aiDirector[0],self.AIVector[1] + aiDirector[1]]

            if self.AIVector == [0,0]:
                self.AIState = 0
            else:
                return self.AIVector
        
        movementNumbers = []
        for i in self.movements:
            newPosition = [currentPosition[0] + i[0], currentPosition[1] + i[1]]
            newPositionObject = checkSquare(board,newPosition)
            newPositionAIObject = checkSquare(aBoard,newPosition)
            
            if newPositionObject in creatureObjects:
                if creatures[creatureObjects.index(newPositionObject)].health > 0:
                    return i
            elif newPositionAIObject in ["u","l","d","r"]:
                newPositionAIObject = "5"

            for x in range(int(newPositionAIObject)):
                movementNumbers.append(i)
                
        return random.choice(movementNumbers)
            

    #finish this function so the monsters move on the board
    def monstersTurn(self,board,aBoard):
        direction = self.AI(board,aBoard)
        board = self.moveCreature(board,direction)
        return board

    # finish this function so that the hero can be moved by using keys
    def moveCreature(self,board,direction):

        currentPosition = getObjectPosition(board,self.object)
        newPosition = [currentPosition[0] + direction[0], currentPosition[1] + direction[1]]
        newPositionObject = checkSquare(board,newPosition)

        if newPositionObject == " ":
            board = setObjectPosition(board,self.object,newPosition,currentPosition)

        # Change to involve other special spaces
        if newPositionObject == "?":
            self.health += 20
            board = setObjectPosition(board," ",newPosition,newPosition)

        # CHANGE to involve all the creature classes
        elif newPositionObject in creatureObjects:
            fightMonster(board,creatures[creatureObjects.index(newPositionObject)],self)

        return board

    def useItem(self):
        if self.inventory.item.uses > 0:
            if self.inventory.item.heal > 0:
                self.health += self.inventory.item.heal
            self.inventory.item.uses -= 1

            if self.inventory.item.uses == 0:
                self.inventory.item = iNone

