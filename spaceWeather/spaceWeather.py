# Program get day, coordinates of corners of area and coefficient. It calculate average of each cell of area with previous days values then compare average values with day values then write in txt file all day values that more than average*coefficient
import warnings
import numpy as np
import ionex
days=1     # this variable show how many days before will be used to calculate average. It should be 27
koefficient=1
n=73
m=71
mas=[0]*n
for i in range(n):
    mas[i]=[0]*m
output=open("output.txt","w")
output.write("Date \n")
output.write("TEC of area  |  difference between area's TEC and area's mediana  |  coordinates of area \n \n")
print("Enter the year(2 last digits) and number of day (For example 15 77 means 77'th day (18 of march) of 2015 year)")
s=input()
s=s.split()
year=int(s[0])
day=int(s[1])
daynow=0
print("Enter the top left and bottom right corner of the area (x1 y1 x2 y2) without any symbols. Each coordinate is number of row and column")
s1=input()
s1=s1.split()
x1=int(s1[0])
y1=int(s1[1])
x2=int(s1[2])
y2=int(s1[3])
if (x1>73):
    x1=73
if (x2>73):
    x2=73
if (x1<0):
    x1=0
if (x2<0):
    x2=0
if(y1>71):
    y1=71
if(y1<0):
    y1=0
if(y2>71):
    y2=71
if(y2<0):
    y2=0
print("your coordinates: [",(x1*5)-180,"; ",87.5-(y1*2.5),"], [", (x2*5)-180,"; ",87.5-(y2*2.5),"]")
print("Enter the difference сoefficient (it means how many times sotrm's TEC must be more then normal TEC)")
koefficient=int(input())
start=73*y1+x1
length=abs(x2-x1)
height=abs(y1-y2)
mas1=[0]*height
med=[0]*height
for i in range(height):
    mas1[i]=[0]*length
    med[i]=[0]*length


for i in range(days):
        daynow=int(day-i-1)
        try:
            with open("ckmg0"+str(daynow)+"0."+str(year)+"i") as file:
                inx = ionex.reader(file)
                for ionex_map in inx:
                    k=0;
                    for i in range(height):
                       for j in range(length):
                           med[i][j]=med[i][j]+int(ionex_map.tec[start+j+i*73]*10)
        except:
            print("day doesn't exist")

for i in range(height):
    for j in range(length):
        med[i][j]=int(med[i][j]/(days*25)) #average calculates as ariphmetic average(not as mediana) because Python is very slow
        print(med[i][j], end=" ")
    print()
try:
    with open("ckmg0"+str(day)+"0."+str(year)+"i") as file:
                inx = ionex.reader(file)
                #print(inx.height)
                for ionex_map in inx:
                    k=0
                    #  print(ionex_map.epoch)
                    output.write(str(ionex_map.epoch)+"\n")
                    for i in range(height):
                        for j in range(length):
                            mas1[i][j]=int(ionex_map.tec[start+j+i*73]*10)
                            if mas1[i][j]>med[i][j]*koefficient:
                                output.write(str(mas1[i][j])+"  "+str(abs(mas1[i][j]-med[i][j]))+"\t ["+str(((x1+i)*5)-180)+"; "+str(87.5-((y1+j)*2.5))+"] \n")
                                k=1
                    if k==1:
                        output.write("\n")
except:
    print("ERROR")

output.close()
print()