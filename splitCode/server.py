# SERVER
import * from rogueClasses.py
import random
import threading
import os
from socket import *
import pickle
from io import BytesIO

# // FUNCTIONS // #

# creates the item lists
def createWeightedList(items):
    itemList = []
    for i in items:
        for x in range(i.rarity):
            itemList.append(i)

    return itemList

# gets the map from the given filename
def getMap(filename)
    f = open(filename,"r")
    layoutContents = f.read()
    layoutContents = layoutContents.split("//")
    f.close()

    vBoard = genBoard(layoutContents[0])
    aBoard = genBoard(layoutContents[1])

    return vBoard,aBoard
    
# turns the board strings into a 2d array
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

# Finds specific objects on the board
def getObjectPosition(board,object):
    for y,row in enumerate(board):
        for x, thing in enumerate(row):
            if thing == object:
                position = [x,y]
    return position

#sets a new position for an object
def setObjectPosition(board,object,newPosition,oldPosition):
    board[oldPosition[1]][oldPosition[0]] = ' '
    board[newPosition[1]][newPosition[0]] = object
    return board

# checks what is in a square
def checkSquare(board,newPosition):
    square = board[newPosition[1]][newPosition[0]]
    return(square)

# NEEDS CHANGING TO ACCOMODATE PLAYER LOOTING ITEMS 'N ALL
# finish this function so the hero "O" can fight the monsters
def fightMonster(board,monster,creature):
    monster.health -= (creature.damage*creature.inventory.weapon.damage) / (monster.damageReductor * monster.inventory.armour.reduction)
    if monster.health <= 0:
        board = setObjectPosition(board," ",getObjectPosition(board,monster.object),getObjectPosition(board,monster.object))
        creature.inventory.swapItems(monster.inventory,creature)

    return board

# Runs the game, MIGHT NEED REWORKING *SLIGHTLY*
def mainLoop():
    while player.health > 0:
        for c in creatures:
            if c.health > 0:
                board = c.move(vBoard,aBoard)

        print('\n'*100)

    # PUT INTO MAINLOOP
    threads = []
    for p in playerWorkers:
        t = threading.Thread(target = worker)
        threads.append(t)
        t.start()


# Network functions:

# // VARIABLES // #

# thread boilerplate
#we can probably turn playerWorkers into a structure containing the player objects? Then pass that into the thread on L267
playerWorkers = 1

# boards
vBoard,aBoard = getMap("layout.txt")

# item lists
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
#creates the weighted lists using my totally orginal function
wR = createWeightedList([wNone,wWood,wStone,wIron,wSteel,wSmax])
aR = createWeightedList([aNone,aWood,aLeather,aIron,aSteel])
iR = createWeightedList([iNone,iHealth1,iHealth2,iCharm1])

# creatures
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

# Create individual threads for players
def worker():
    # do stuff on a thread
    print("Multi-threaded printing lads")
    return


mainloop()
