import os

rooms = []

for root, dirs, files in os.walk("rooms"):
    # GETS THE LAYOUT FROM THE GIVEN TEXT FILE
    for n in files:
        f = open("rooms/" + n,"r")
        roomContents = f.read()
        roomContents = roomContents.split("//")

        print(roomContents[0])
        
        rooms.append(roomContents)
        f.close()
