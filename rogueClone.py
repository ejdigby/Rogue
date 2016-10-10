# GET CREATURE.printStats working
import random
import os
os.environ['LINES'] = '40'
os.environ['COLUMNS']= '80'

# HERO : O
# MONSTERS : A, B, C, D, E, F
# WALLS : X
# HEALING SHRINES : ?

# GETS THE LAYOUT FROM THE GIVEN TEXT FILE
f = open("layout.txt","r")
layoutContents = f.read()
layoutContents = layoutContents.split("//")
f.close()


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
        

wNone = Weapon(1,"None","No weapon",24)
wWood = Weapon(1.5,"Wooden Sword","Wooden",45)
wStone = Weapon(2,"Stone Sword","Meh",30)
wIron = Weapon(3,"Iron Sword","Decent",15)
wSteel = Weapon(4,"Steel Sword","Good",9)
wSmax = Weapon(10,"Fists of Smaximus","Ouch",1)

aNone = Armour(1,"None","No armour",8)
aWood = Armour(2,"Wooden Armour","Wooden",15)
aLeather = Armour(3,"Leather Armour","Meh",10)
aIron = Armour(5,"Iron Armour","Good",5)
aSteel = Armour(6,"Steel Armour","Slightly worn",2)

iNone = Item(0,1,1,"None","No items",0,20)
iHealth1 = Item(20,1,1,"Small Health Potion","Heals 20 health",1,5)
iHealth2 = Item(50,1,1,"Health Potion","Heals 50 health",1,1)
iCharm1 = Item(0,2,0.8,"Thing","Ups dmg, lowers armour",5,2)


###Beginning of loot distribution
# NAME, DAMAGE / REDUCTION, RARITY, TYPE
# TYPE : 0 - armour, 1 - weapon

weapons = [wNone,wWood,wStone,wIron,wSteel,wSmax]
wR = []

armour = [aNone,aWood,aLeather,aIron,aSteel]
aR = []

items = [iNone,iHealth1,iHealth2,iCharm1]
iR = []

for w in weapons:
    for x in range(w.rarity):
        wR.append(w)
for a in armour:
    for x in range(a.rarity):
        aR.append(a)
for i in items:
    for x in range(i.rarity):
        iR.append(i)





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
                take = False
                while take == False:
                    print("You can take the item : " + otherInv.item.name)
                    take = input("Do you want to take this item? [y/n]: ").lower()
                    if take == "y":
                        self.item = otherInv.item
                    elif take != "n":
                        take = False
                        print("That was invalid input, please pick again")

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
        allActions = ['w','a','s','d','i',"yea boiiiiiii"]
        action = 0
        while action not in allActions:
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

    #def printStats(self):
        

    
## THESE GLOBAL VARIABLE DECIDE THE MONSTER AND PLAYER CREATURES
player = Creature("O",True,200,1,25,[[0,-1],[-1,0],[0,1],[1,0]],Inventory(wWood,aWood,iHealth1))
A = Creature("A",False,100,1,10,[[0,-1],[-1,0],[0,1],[1,0]],Inventory(random.choice(wR),random.choice(aR),random.choice(iR)))
B = Creature("B",False,120,1,10,[[0,-1],[-1,0],[0,1],[1,0]],Inventory(random.choice(wR),random.choice(aR),random.choice(iR)))
C = Creature("C",False,140,1,10,[[0,-1],[-1,0],[0,1],[1,0]],Inventory(random.choice(wR),random.choice(aR),random.choice(iR)))
D = Creature("D",False,160,1,10,[[0,-1],[-1,0],[0,1],[1,0]],Inventory(random.choice(wR),random.choice(aR),random.choice(iR)))
E = Creature("E",False,180,1,10,[[0,-1],[-1,0],[0,1],[1,0]],Inventory(random.choice(wR),random.choice(aR),random.choice(iR)))
F = Creature("F",False,200,1,10,[[0,-1],[-1,0],[0,1],[1,0]],Inventory(random.choice(wR),random.choice(aR),random.choice(iR)))
creatures = [player,A,B,C,D,E,F]
creatureObjects = []
for c in creatures:
    creatureObjects.append(c.object)

def genBoard(layout):
    #This function generates the board - do not change it
    board = []
    row = []
    for i in layout:
        row.append(i)
        if i == '\n':
            board.append(row)
            row = []
    return board

def printBoard(board):
    #This function prints the board - do not change it
    for row in board:
        for character in row:
            print(character, end=" ")
    
def getObjectPosition(board,object):
    # Finds specific objects on the board
    for y,row in enumerate(board):
        for x, thing in enumerate(row):
            if thing == object:
                position = [x,y]
    return position

def setObjectPosition(board,object,newPosition,oldPosition):
    #sets a new position for an object
    board[oldPosition[1]][oldPosition[0]] = ' '
    board[newPosition[1]][newPosition[0]] = object
    return board

def checkSquare(board,newPosition):
    # checks what is in a square
    square = board[newPosition[1]][newPosition[0]]
    return(square)

# finish this function so the hero "O" can fight the monsters
def fightMonster(board,monster,creature):
    monster.health -= (creature.damage*creature.inventory.weapon.damage) / (monster.damageReductor * monster.inventory.armour.reduction)
    if monster.health <= 0:
        board = setObjectPosition(board," ",getObjectPosition(board,monster.object),getObjectPosition(board,monster.object))
        creature.inventory.swapItems(monster.inventory,creature)

    return board

# placeholder for creature.printstats()
def printStats(creature):
    print(creature.object + ": " + str(creature.health) + ", " + str(creature.AIState) + ", " + str(creature.AIVector))
    print(creature.object + " inv: " + creature.inventory.weapon.name + ", " + creature.inventory.armour.name + ", " + creature.inventory.item.name)

def mainLoop():
    # Runs the game
    while player.health > 0:
        for c in creatures:
            if c.health > 0:
                printStats(c)

        printBoard(vBoard)
        for c in creatures:
            if c.health > 0:
                board = c.move(vBoard,aBoard)

        print('\n'*100)

# vBoard : visible
# aBoardBase : AI-base
# aBoard : AI viewable
vBoard = genBoard(layoutContents[0])
aBoard = genBoard(layoutContents[1])

mainLoop()
