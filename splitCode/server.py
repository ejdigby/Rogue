# SERVER
from rogueClasses import *
import random
import threading
import os
from socket import *
import pickle
from io import BytesIO

# // FUNCTIONS // #

# gets the map from the given filename
def getMap(filename):
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

# Runs the game, MIGHT NEED REWORKING *SLIGHTLY*
def mainLoop():
    # once enough client connections have been made
    while running:
        for p in playerConnections:
            # using placeholder functions and variables
            if p.creature.health > 0:
                board = p.move(p.keyStroke)
        for c in creatures:
            if c.health > 0:
                board = c.move(vBoard,aBoard)

    '''
    # PUT INTO MAINLOOP
    threads = []
    for p in playerWorkers:
        t = threading.Thread(target = worker)
        threads.append(t)
        t.start()
    '''

# // VARIABLES // #
# boards
vBoard,aBoard = getMap("layout.txt")

mainLoop()
