import math
import pygame
import random
import csv
from pendulum import *
from magnet import *
import statistics 
import datetime
from PIL import Image
import numpy as np
import sys
# create fractal image
np.set_printoptions(precision=10)

# screen constants
WIDTH = 600
HEIGHT = 600


fnetList = []

# List of magnets
magnets = []

# Pendulum
pend = Pendulum(0, 0, 1, 0.000005, 0.008, 6)

# Number of magnets
n =random.randint(2,4)

pygame.init()
#screen = pygame.display.set_mode((WIDTH, HEIGHT))


isStationary=False
isFractalMode = True
isDisplayWhileGenerating = False
clock = pygame.time.Clock()
dt = clock.tick(600)


# pendulum parameters

MASS = 1
k = 0.00005
FRICTION = 0.00008
STEPS = 2

# magnet parameters
STRENGTH = 400
# initialize magnets
#for i in range(n):
#    magnets.append(Magnet(random.randint(0,WIDTH), random.randint(0,HEIGHT), 500))
    #magnets.append(Magnet(WIDTH//2+100, HEIGHT//2+100, 500))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
dt = clock.tick(600)


x = 0
done = False
flip = False
def distance(x1,y1, x2,y2):
    return math.sqrt((y2-y1)**2+(x2-x1)**2)

while not done:
        n =random.randint(2,6)
        
        img = Image.new("RGBA", (WIDTH,HEIGHT),(256,256,256))
        magnets = []
        timeArray = np.zeros((WIDTH,HEIGHT, 3), dtype = np.double)

        random.seed()
        maxTime = 0
        for a in range(n):
            magnets.append(Magnet(random.randint(0,WIDTH), random.randint(0,HEIGHT), random.randint(int(0.1*STRENGTH), STRENGTH)))
        # always add a magnet at the middle
        #magnets.append(Magnet(WIDTH/2, HEIGHT/2, STRENGTH))
        n = len(magnets)
        data = np.zeros((WIDTH, HEIGHT, 3+n), dtype='uint8')
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if (i == 0 and j == 0):
                    print("here")
                    print(pend.Fnet_x)
                    flip = True
                pend = Pendulum(j, i, MASS, k, FRICTION, STEPS)
                time = 0
                isStation = False
                while not isStation:
                    isStation = pend.update(WIDTH, HEIGHT, magnets, dt, isStation)


                    time+=1
                

                data[j][i][0] = pend.lastColour[0]
                data[j][i][1] = pend.lastColour[1]
                data[j][i][2] = pend.lastColour[2]
                maxTime = max(time,maxTime)

                for x in range(n):
                    if pend.lastColour == magnets[x].colour:
                        data[j][i][3+x] = time
                #print(data[j,i])
                #print(str(pend.lastColour[0]) + ", " + str(int(min(255, pend.lastColour[0]*(1+distance(j,i,pend.x,pend.y)/distance(0,0,WIDTH,HEIGHT))))))

                # shading by distance
                #img.putpixel((j,i), (int(min(255, pend.lastColour[0]*(1+distance(j,i,pend.x,pend.y)/distance(0,0,WIDTH/2,HEIGHT/2)))),
                #                             int(min(255, pend.lastColour[1]*(1+distance(j,i,pend.x,pend.y)/distance(0,0,WIDTH/2,HEIGHT/2)))),
                #                             int(min(255, pend.lastColour[2]*(1+distance(j,i,pend.x,pend.y)/distance(0,0,WIDTH/2,HEIGHT/2))))))

                # shading by maxtime
            print("[" + str(j) + ", " + str(i))
            #print("maxtime is : " + str(maxTime))
        #print(list(img.getdata()))
        #print(data)
        #timeArray = timeArray - timeArray.mean()
        #timeArray = (timeArray/timeArray.max())
        #newData = data
        maxArr = np.zeros((n,2))
  
        maxArr =np.amax(data.reshape(WIDTH*HEIGHT,n+3), axis=0)
        print(maxArr)
        #print(data[:,:,[2,3]])
        #print(data.shape[0])
        for o in range(data.shape[0]):
            for p in range(data.shape[1]):
                for m in range(len(magnets)):
                    if (data[o,p,0]==magnets[m].colour[0] and data[o,p,1]==magnets[m].colour[1] and data[o,p,2]==magnets[m].colour[2]):
                        floatMax = data[o,p,3+m]/maxArr[3+m]
                        #print(floatMax)
                        #print(data[p,o,3+m])
                        #print(data[p,o,0])
                        #print("orig is: " + str(data[o,p,2+m]))
                        img.putpixel((o,p,), (int(min(255,data[o,p,0]*floatMax)),
                                                  int(min(255,data[o,p,1]*floatMax)),
                                                  int(min(255,data[o,p,2]*floatMax))))
                        #("end " +str(data[p,o,0]))
                        #print("now is: " + str(data[o,p,2+m]))
            #newData = (data[:,:,0]==magnets[n].colour[0] and data[:,:,1]==magnets[n].colour[1] and data[:,:,2]==magnets[n].colour[0]).astype(int) 
            
            #data = np.where(np.isin(data,[0,1,3,16,17,18]),arr+1,0)

        #for i in range(data.shape[0]):
            
        #print(data[0,0])

        #img = Image.fromarray(data[:,:,0:2], mode='RGB')
        #img = img.convert("RGB")
        img.save("D:/Documents/PythonProjects/Magnetic Pendulum/images/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".bmp")
        img.close()
        magnets.clear()
        x+=1
        
        # miscellaneous logging
        #with open("mlist.csv","a") as f:
        #    writer = csv.writer(f,delimiter=",")
        #    writer.writerow([clock.get_time(),pend.M_x])
