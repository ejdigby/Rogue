#server
from socket import *
import threading
import pickle
from io import BytesIO

#TODO: needs to test the buffer size.
# If too large, a loop may needed to read all buffer content

# TEST DICTIONARY
class AbsoluteG():
    def __init__(self):
        self.a = "aaaaaa"
        self.ga = "gaaaaaa"
        self.r = "rerererererepiratererere"

SIZE = 1024

soc = socket(AF_INET,SOCK_STREAM)
soc.bind(('127.0.0.1',5432))
soc.listen(9)

class RecThread(threading.Thread):
    def __init__(self,soc):
        threading.Thread.__init__(self)
        self.soc = soc
        self.RunningState=True

    def iRecieve(self):
        data = self.soc.recv(SIZE)
        return data

    def run(self):
        while self.RunningState:
            msg = self.iRecieve()
            robo = pickle.loads(msg)
            print ('Recieved->  ' + robo.a)
            print(robo.ga)
            print(robo.r)

def setupConn(con1,con2):
    connTypes={}
    state = con1.recv(4)  
    if state =='RECV':
        connTypes['send'] = con1 
        connTypes['recv'] = con2
    else:
        connTypes['recv'] = con1 
        connTypes['send'] = con2
    return connTypes

def iSend(conn,msg):
    if len(msg)>0:
        conn.sendall(msg.encode())
        print("Sent->  ", msg)

(soc1,addr1) = soc.accept()
(soc2,addr2) = soc.accept()

connTypes = setupConn(soc1,soc2)
thrd = RecThread(connTypes['recv'])
thrd.start()

while True:
        iSend(connTypes['send'],input())

