import socket
import numpy as np
import matplotlib.pyplot as plt
import struct


host = "84.237.21.36"
port = 5152

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

plt.ion()
plt.figure()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))

    beat = b"nope"
    
    while beat != b"yep":

        sock.send(b"get")
        bts = recvall(sock, 40002)

        img = np.frombuffer(bts[2:], dtype="uint8").reshape(bts[0], bts[1])
        
        a=np.argmax(img)
        pos = np.unravel_index(a, img.shape)

        width = 1
        height = 1
        size = [width, height]
        pixel_colors = []
        max1=0
        max2=0
        max1i=[-1,-1]
        max2i=[-1,-1]
        pos=[0,0]
        next_pos=[0,0]
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
        pos=(max1i[0], max1i[1])
        next_pos=(max2i[0], max2i[1])
        delta = np.abs(np.array(pos)-np.array(next_pos))
        res1 = np.sqrt((pos[0]-next_pos[0])**2+(pos[1]-next_pos[1])**2)
        res = np.sqrt(delta[0]*delta[0]+delta[1]*delta[1])
        res = round(res ,1)
        sock.send(f'{res}'.encode())
        print(sock.recv(20))

        plt.clf()
        plt.suptitle(f'delta = {str(delta)}, distance = {res}')
        plt.title(str(pos)+', '+str(next_pos))
        plt.imshow(img)

        plt.pause(0.3)

        sock.send(b"beat")
        beat = sock.recv(20)

print("Done!")


