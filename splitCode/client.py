# DOING OBJECTS WITHIN OBJECTS
# RECEIVING OBJECT THAT CONTAINS:
# map
# creature health
# player inventory

import os
from socket import *
import threading
from Robot import Robot
import pickle
from io import BytesIO

SIZE =1024

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




soc1 = socket(AF_INET,SOCK_STREAM)
soc1.connect(('127.0.0.1',5432))
soc1.send('SEND'.encode()) # telling server we will send data from here

soc2 = socket(AF_INET,SOCK_STREAM)
soc2.connect(('127.0.0.1',5432))
soc2.send('RECV'.encode()) # telling server we will recieve data from here

def iSend(conn,msg):
    conn.sendall(msg)
    print("Sent->  ", msg)

thrd = client(soc2)
thrd.start()
#data is the data to be sent
iSend(soc1, pickle.dumps(data))

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
    
    
