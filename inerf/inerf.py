"""
import socket
import numpy as np
import matplotlib.pyplot as plt

host = "84.237.21.36"
port = 5151

def recvall(sock, n):
    data = bytearray()
    while len(data)<n:
        packetik=sock.recv(n-len(data))
        if not packetik:
            return None
        data.extend(packetik)
    return(data)
plt.ion()
plt.figure()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat =b"nope"
    while beat !="yep":

        sock.send(b"get")
        bts = recvall(sock, 80004)
        rows = bts[0]
        cols=bts[1]
        img1=bts[2:40002]
        img1=np.frombuffer(img1, dtype="uint8").reshape(rows,cols)
        rows = bts[40002]
        cols=bts[40003]
        img2=bts[40004:]

        img2=np.frombuffer(img2, dtype="uint8").reshape(rows,cols)


        pos1=np.unravel_index(np.argmax(img1),img1.shape)
        pos2=np.unravel_index(np.argmax(img2),img2.shape)

        delta = np.abs(np.array(pos1)-np.array(pos2))
        sock.send(f"{delta[0]}{delta[1]}".encode())
        print(sock.recv(10))


        plt.clf()
        plt.suptitle(f"delta={str(delta)}")
        plt.subplot(121)
        plt.title(str(pos1))
        plt.imshow(img1)
        plt.subplot(122)
        plt.title(str(pos2))
        plt.imshow(img2)
        plt.pause(0.1)
       # plt.show()

        sock.send(b"beat")
        beat=sock.recv(10)

print("Done")
"""

import socket
import numpy as np
import matplotlib.pyplot as plt

host = "84.237.21.36"
port = 5152

def recvall(sock, n):
    data = bytearray()
    while len(data)<n:
        packetik=sock.recv(n-len(data))
        if not packetik:
            return None
        data.extend(packetik)
    return(data)
plt.ion()
plt.figure()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat =b"nope"
    while beat !="yep":

        sock.send(b"get")
        bts = recvall(sock, 40002)
        img=np.frombuffer(bts[2:], dtype="uint8").reshape(bts[0],bts[1])
        oldmax=0
        oldmax=[-1,-1]
        max1=0
        max2=0
        max1i=[-1,-1]
        max2i=[-1,-1]
        for i in range(len(img)):
            for j in range(len(img[i])):
                if img[i][j]>=max1:  
                    max1=img[i][j]
                    max1i[0]=i
                    max1i[1]=j
        rad=0.0
        for i in range(len(img[0]-max1i[0])):
            if img[max1i[0]+i][max1i[1]]!=0:
                rad=rad+1
            else:
                break
        for i in range(len(img)):
            for j in range(len(img[i])):
                if img[i][j]>=max2 and (((max1i[1]-j)**2+(max1i[0]-i)**2)**0.5>rad):  
                    max2=img[i][j]
                    max2i[0]=i
                    max2i[1]=j

        print(max1i," ",max2i)
        if max2i[0]!=-1:
            delta = ((max2i[1]-max1i[1])**2+(max2i[0]-max1i[0])**2)**0.5
            delta=f"{delta:.{1}f}"
        else:
            delta=0.0
        print(delta)

        #res=b"1.41"
        sock.send(f"delta".encode())
        #sock.send(res)
        print(sock.recv(20))
        plt.clf()
        plt.imshow(img)
        plt.pause(0.5)
        print()
        sock.send(b"beat")
        beat=sock.recv(20)

print("Done")
