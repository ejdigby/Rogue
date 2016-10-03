import random
import os
import sys
import time
os.environ['LINES'] = '40'
os.environ['COLUMNS']= '80'
###Beginning of loot distribution
potentialLootRare = [['iron_sword',1.6,32,'weapon'],
                 ['steel_sword',1.8,15,'weapon'],
                 ['iron_chestplate',4.6,32,'armour'],
                 ['steel_chestplate',4.8,15,'armour']
]
potentialLootCommon = [['wooden_sword',1.2,60,'weapon'],
                 ['stone_sword',1.4,50,'weapon'],
                 ['wooden_chestplate',4.2,60,'armour'],
                 ['leather_chestplate',4.4,50,'armour']
]
populationCommon = []
populationRare = []
for i in potentialLootRare:
    for j in range(i[2]):
        populationRare.append(i)
        if j % 6 == 0:
            populationRare.append(' ')
for i in potentialLootCommon:
    for j in range(i[2]):
        populationCommon.append(i)
def is_float(num):
    try:
        float(num)
        return True
    except:
        return False
###CLASSES FOR MONSTER
class Monster:
    def __init__(self, name, hp, inv, dam):
        self.name = name
        self.hp = hp
        self.inv = inv
        self.dam = dam
    def attack(self, dam):
        print("Monster " + self.name + " is attempting to attack!")
        return dam
def moveMonsters(board):
    '''This function moves monsters around the board'''
    totalMonsters = [A,B,C,D,E,F,G]
    for m in totalMonsters:
        if is_float(m.hp) == False:
            pass
        else:
            #print(m.hp)
            objectPosition = getObjectPosition(board, m.name)
            newPosition = [(objectPosition[0] + random.randint(-1,1)), (objectPosition[1] + random.randint(-1,1))]
            newPositionValue = checkSquare(board, newPosition)
            if newPositionValue == " ":
                board = setObjectPosition(board,m.name,newPosition,objectPosition)
            else:
                pass
    return board
###Initialising monster objects
A = Monster("A", 20, [random.choice(populationCommon)], 2)
B = Monster("B", 30, [random.choice(populationCommon)], 4)
C = Monster("C", 25, [random.choice(populationCommon)], 3)
D = Monster("D", 35, [random.choice(populationRare)], 5)
E = Monster("E", 40, [random.choice(populationRare)], 6)
F = Monster("F", 45, [random.choice(populationRare)], 7)
G = Monster("G", 50, [random.choice(populationRare)], 8)
###CLASS FOR PC
class Player:
    def __init__(self, hp, inv, dt, baseDam, armour):
        self.hp = hp
        self.inv = inv
        self.dt = dt
        self.baseDam = baseDam
        self.armour = armour
    def attack(self,baseDam, weapon):
        print("Player is attacking")
        return baseDam * weapon
###Initialising player object
Ohm = Player(35, [], 4, 3, 'none')
##HERE IS THE BOARD - YOU CAN EDIT IT TO CHANGE THE LAYOUT OF THE ROOMS, POSITIONS OF MONSTERS AND POSITIONS OF HEALING SHRINES
layout='''___________________________________________________________________________
|XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|
|XXXX      XXXXXXXXXXXXX      A        XXXXXXXXXXXXX       ?    X      XXX|
|XXXX      XXXXXXXXXXXXX               XXXXXXXXXXXXX  XXXXXXXX  X  B   XXX|
|XXXX                                  XXXXXXXXXX      XXXXXXX         XXX|
|XXXX      XXXXXXXXXXXXX        O                      XXXXXXXXXXXXXXXXXXX|
|XXXXXXXXXXXXXXXXXXXXXXX               XXXXXXXXXX   C  XXXXXXXXXXXXXXXXXXX|
|XXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXX        XXXXX|
|XXXXXX                 XXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXX   G    XXXXX|
|XXXXXX  XXXXX  XXXX   ?XXXXXX  XXXXXXXXXXXXXXXXX      XXXXXX        XXXXX|
|XXXXXX  XXXXX  XXXXXXXXXXXXXX ?XXXXXXXXXXXXXXXXX  D   XXXXXXXXXXXX  XXXXX|
|XXXXXX  XXXXX                                         XXXX          XXXXX|
|XXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      XXXX     XXXXXXXXXX|
|XXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  ?  XXXXXXXXXX|
|XXXXXX       E       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXX|
|XXXXXXXXXXXXXX   F                                             XXXXXXXXXX|
|XXXXXXXXXXXXXX       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|
|XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|
|-------------------------------------------------------------------------|
'''
def bestWeapon(inventory):
    #Separate the weapons and armour using the listComp below
    best = [['',0,0,'']]
    wInventory = [x for x in inventory if x != ' ' or x != [''] or x != [' ']]
    if wInventory == []:
        return [['fists', 1, 0]]
    for i in wInventory:
        if len(i) == 1:
            wInventory.remove(i)
        elif i[0][3] != 'weapon':
            wInventory.pop(i.index(i[0]))
    for i in wInventory:
        if i[0][1] > best[0][1]:
            best = i
    return i
def genBoard():
    '''This function generates the board - do not change it'''
    board = []
    row = []
    for i in layout:
        row.append(i)
        if i == '\n':
            board.append(row)
            row = []
    return board
def printBoard(board):
    '''This function prints the board - do not change it'''
    for row in board:
        for character in row:
            print(character, end=" ")
def playerTurn(board):
    '''This function decides on players actions - you could potentially add more actions in here'''
    action = input('What do you want to do? Type "help" for a list of keybindings: ')
    keys = ['w','a','s','d']
    movements = [[0,-1],[-1,0],[0,1],[1,0]]
    if action.lower() in keys:
        #print("Attempting movement number 1...")
        board = move(board,'O',movements[keys.index(action.lower())])
    if action.lower() == 'help':
        print("\nW: Moves Ohm one character up \n")
        print("A: Moves Ohm one character left \n")
        print("S: Moves Ohm one character down \n")
        print("D: Moves Ohm one character right \n")
        print("Interaction, attacking and movement are all bundled into one, move into a monster? Attacked it. Moved into a healing shrine? Healed etc etc")
        print("Healing shrines are one use only and will restore you to full health")
        print("Picked up some cool loot? Ohm will automatically equip and use the best equipment he has")
    return board
def playerDead(health):
    if health < 0:
        return True
    else:
        return False
def move(board,object,direction):
    objectPosition = getObjectPosition(board, object)
    print("O's position is: " + str(objectPosition))
    newPosition = [(objectPosition[0] + direction[0]), (objectPosition[1] + direction[1])]
    print("He is attempting to end up at this position: " + str(newPosition))
    newPositionValue = checkSquare(board, newPosition)
    if newPositionValue == "?":
        print("You've entered a healing shrine!")
        Ohm.hp = 35
        print("Your health has been restored to full!")
        board[newPosition[1]][newPosition[0]] = " "
    elif newPositionValue in ["A","B","C","D","E","F","G"]:
        if newPositionValue == "A":
            print(bestWeapon(Ohm.inv))
            A.hp -= Ohm.attack(Ohm.baseDam, bestWeapon(Ohm.inv)[0][1])
            if A.hp < 0:
                print("You've killed the monster!")
                positionOfA = getObjectPosition(board, "A")
                board[positionOfA[1]][positionOfA[0]] = " "
                A.hp = "You've managed to slay this monster!"
                if A.inv != ' ':
                    if A.inv != [' ']:
                        for i in A.inv:
                            if i[3] == 'armour' and i[1] > float(Ohm.dt):
                                Ohm.dt = i[1]
                                Ohm.armour = i[0]
                    Ohm.inv.append(A.inv)
                A.inv = "nothing, you've looted its body."
            else:
                Ohm.hp -= A.attack(A.dam) / float((Ohm.dt / 2) - 1)
                if playerDead(Ohm.hp):
                    print("You died! Better luck next time!")
                    print("\n Exiting in 5...")
                    time.sleep(1)
                    print("\n Exiting in 4...")
                    time.sleep(1)
                    print("\n Exiting in 3...")
                    time.sleep(1)
                    print("\n Exiting in 2...")
                    time.sleep(1)
                    print("\n Exiting in 1...")
                    time.sleep(1)
                    sys.exit()
        if newPositionValue == "B":
            B.hp -= Ohm.attack(Ohm.baseDam, bestWeapon(Ohm.inv)[0][1])
            if B.hp < 0:
                print("You've killed the monster!")
                positionOfB = getObjectPosition(board, "B")
                board[positionOfB[1]][positionOfB[0]] = " "
                B.hp = "You've managed to slay this monster!"
                if B.inv != ' ':
                    if B.inv != [' ']:
                        for i in B.inv:
                            if i[3] == 'armour' and i[1] > float(Ohm.dt):
                                Ohm.dt = i[1]
                                Ohm.armour = i[0]
                        Ohm.inv.append(B.inv)
                B.inv = "nothing, you've looted its body."
            else:
                Ohm.hp -= B.attack(B.dam) / float((Ohm.dt / 2) - 1)
                if playerDead(Ohm.hp):
                    print("You died! Better luck next time!")
                    print("\n Exiting in 5...")
                    time.sleep(1)
                    print("\n Exiting in 4...")
                    time.sleep(1)
                    print("\n Exiting in 3...")
                    time.sleep(1)
                    print("\n Exiting in 2...")
                    time.sleep(1)
                    print("\n Exiting in 1...")
                    time.sleep(1)
                    sys.exit()
        if newPositionValue == "C":
            C.hp -= Ohm.attack(Ohm.baseDam, bestWeapon(Ohm.inv)[0][1])
            if C.hp < 0:
                print("You've killed the monster!")
                positionOfC = getObjectPosition(board, "C")
                board[positionOfC[1]][positionOfC[0]] = " "
                C.hp = "You've managed to slay this monster!"
                if C.inv != ' ':
                    if C.inv != [' ']:
                        for i in C.inv:
                            if i[3] == 'armour' and i[1] > float(Ohm.dt):
                                Ohm.dt = i[1]
                                Ohm.armour = i[0]
                    Ohm.inv.append(C.inv)
                C.inv = "nothing, you've looted its body."
            else:
                Ohm.hp -= float(C.attack(C.dam)) / float((Ohm.dt / 2) - 1)
                if playerDead(Ohm.hp):
                    print("You died! Better luck next time!")
                    print("\n Exiting in 5...")
                    time.sleep(1)
                    print("\n Exiting in 4...")
                    time.sleep(1)
                    print("\n Exiting in 3...")
                    time.sleep(1)
                    print("\n Exiting in 2...")
                    time.sleep(1)
                    print("\n Exiting in 1...")
                    time.sleep(1)
                    sys.exit()
        if newPositionValue == "D":
            D.hp -= Ohm.attack(Ohm.baseDam, bestWeapon(Ohm.inv)[0][1])
            if D.hp < 0:
                print("You've killed the monster!")
                positionOfD = getObjectPosition(board, "D")
                board[positionOfD[1]][positionOfD[0]] = " "
                D.hp = "You've managed to slay this monster!"
                if D.inv != ' ':
                    if D.inv != [' ']:
                        for i in D.inv:
                            if i[3] == 'armour' and i[1] > float(Ohm.dt):
                                Ohm.dt = i[1]
                                Ohm.armour = i[0]
                    Ohm.inv.append(D.inv)
                D.inv = "nothing, you've looted its body."
            else:
                Ohm.hp -= float(C.attack(D.dam)) / float((Ohm.dt / 2) - 1)
                if playerDead(Ohm.hp):
                    print("You died! Better luck next time!")
                    print("\n Exiting in 5...")
                    time.sleep(1)
                    print("\n Exiting in 4...")
                    time.sleep(1)
                    print("\n Exiting in 3...")
                    time.sleep(1)
                    print("\n Exiting in 2...")
                    time.sleep(1)
                    print("\n Exiting in 1...")
                    time.sleep(1)
                    sys.exit()
        if newPositionValue == "E":
            E.hp -= Ohm.attack(Ohm.baseDam, bestWeapon(Ohm.inv)[0][1])
            if E.hp < 0:
                print("You've killed the monster!")
                positionOfE = getObjectPosition(board, "E")
                board[positionOfE[1]][positionOfE[0]] = " "
                E.hp = "You've managed to slay this monster!"
                if E.inv != ' ':
                    if E.inv != [' ']:
                        for i in E.inv:
                            if i[3] == 'armour' and i[1] > float(Ohm.dt):
                                Ohm.dt = i[1]
                                Ohm.armour = i[0]
                    Ohm.inv.append(E.inv)
                E.inv = "nothing, you've looted its body."
            else:
                Ohm.hp -= float(E.attack(E.dam)) / float((Ohm.dt / 2) - 1)
                if playerDead(Ohm.hp):
                    print("You died! Better luck next time!")
                    print("\n Exiting in 5...")
                    time.sleep(1)
                    print("\n Exiting in 4...")
                    time.sleep(1)
                    print("\n Exiting in 3...")
                    time.sleep(1)
                    print("\n Exiting in 2...")
                    time.sleep(1)
                    print("\n Exiting in 1...")
                    time.sleep(1)
                    sys.exit()
        if newPositionValue == "F":
            F.hp -= Ohm.attack(Ohm.baseDam, bestWeapon(Ohm.inv)[0][1])
            if F.hp < 0:
                print("You've killed the monster!")
                positionOfF = getObjectPosition(board, "F")
                board[positionOfF[1]][positionOfF[0]] = " "
                F.hp = "You've managed to slay this monster!"
                if F.inv != ' ':
                    if F.inv != [' ']:
                        for i in F.inv:
                            if i[3] == 'armour' and i[1] > float(Ohm.dt):
                                Ohm.dt = i[1]
                                Ohm.armour = i[0]
                    Ohm.inv.append(F.inv)
                F.inv = "nothing, you've looted its body."
            else:
                Ohm.hp -= float(F.attack(F.dam)) / float((Ohm.dt / 2) - 1)
                if playerDead(Ohm.hp):
                    print("You died! Better luck next time!")
                    sprint("\n Exiting in 5...")
                    time.sleep(1)
                    print("\n Exiting in 4...")
                    time.sleep(1)
                    print("\n Exiting in 3...")
                    time.sleep(1)
                    print("\n Exiting in 2...")
                    time.sleep(1)
                    print("\n Exiting in 1...")
                    time.sleep(1)
                    sys.exit()
        if newPositionValue == "G":
            G.hp -= Ohm.attack(Ohm.baseDam, bestWeapon(Ohm.inv)[0][1])
            if G.hp < 0:
                print("You've killed the monster!")
                positionOfG = getObjectPosition(board, "G")
                board[positionOfG[1]][positionOfG[0]] = " "
                G.hp = "You've managed to slay this monster!"
                if G.inv != ' ':
                    if G.inv != [' ']:
                        for i in G.inv:
                            if i[3] == 'armour' and i[1] > float(Ohm.dt):
                                Ohm.dt = i[1]
                                Ohm.armour = i[0]
                    Ohm.inv.append(G.inv)
                G.inv = "nothing, you've looted its body."
            else:
                Ohm.hp -= float(G.attack(G.dam)) / float((Ohm.dt / 2) - 1)
                if playerDead(Ohm.hp):
                    print("You died! Better luck next time!")
                    print("\n Exiting in 5...")
                    time.sleep(1)
                    print("\n Exiting in 4...")
                    time.sleep(1)
                    print("\n Exiting in 3...")
                    time.sleep(1)
                    print("\n Exiting in 2...")
                    time.sleep(1)
                    print("\n Exiting in 1...")
                    time.sleep(1)
                    sys.exit()
    elif newPositionValue == "X":
        print("You've hit a wall!")
    else:
        print("Attempting movement into empty space...")
        board = setObjectPosition(board, object, newPosition, objectPosition)
    return board
def getObjectPosition(board,object):
    '''Finds specific objects on the board'''
    for y,row in enumerate(board):
        for x, thing in enumerate(row):
            if thing == object:
                print(thing)
                position = [x,y]
    return position
def setObjectPosition(board,object,newPosition,oldPosition):
    '''sets a new position for an object'''
    board[oldPosition[1]][oldPosition[0]] = ' '
    board[newPosition[1]][newPosition[0]] = object
    return board
def checkSquare(board,newPosition):
    'checks what is in a square'''
    square = board[newPosition[1]][newPosition[0]]
    return(square)
def mainLoop():
    '''Runs the game'''
    while True:
        board = board1
        printBoard(board)
        board = playerTurn(board)
        board = moveMonsters(board)
        print('\n'*30)
        #print("It is turn " + str(turns))
        if str(A.hp).isdigit() == False and str(B.hp).isdigit() == False and str(C.hp).isdigit() == False and str(D.hp).isdigit() == False and str(E.hp).isdigit() == False and str(F.hp).isdigit() == False and str(G.hp).isdigit() == False:
            print("You've managed to slay all the monsters in this dungeon! Congratulations!")
            print("\n Exiting in 5...")
            time.sleep(1)
            print("\n Exiting in 4...")
            time.sleep(1)
            print("\n Exiting in 3...")
            time.sleep(1)
            print("\n Exiting in 2...")
            time.sleep(1)
            print("\n Exiting in 1...")
            time.sleep(1)
            sys.exit()
        print("Ohm's HP is: " + str(Ohm.hp))
        print("A's HP is: " + str(A.hp))
        print("And it currently holds " + str(A.inv))
        print("B's HP is: " + str(B.hp))
        print("And it currently holds " + str(B.inv))
        print("C's HP is: " + str(C.hp))
        print("And it currently holds " + str(C.inv))
        print("D's HP is: " + str(D.hp))
        print("And it currently holds " + str(D.inv))
        print("E's HP is: " + str(E.hp))
        print("And it currently holds " + str(E.inv))
        print("F's HP is: " + str(F.hp))
        print("And it currently holds " + str(F.inv))
        print("G's HP is: " + str(G.hp))
        print("And it currently holds " + str(G.inv))
board1 = genBoard()
#print(getObjectPosition(board1, "O"))
mainLoop()
