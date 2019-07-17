import math
import pygame
import random
import csv
from pendulum import *
from magnet import *
import statistics 

from PIL import Image
# create fractal image


# screen constants
WIDTH = 600
HEIGHT = 600

img = Image.new("RGBA", (WIDTH,HEIGHT),(256,256,256))

fnetList = []

# List of magnets
magnets = []

# Pendulum
pend = Pendulum(0, 0, 1, 0.000005, 0.008, 6)

# Number of magnets
n = 6

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


isStationary=False
isFractalMode = False
isDisplayWhileGenerating = False
clock = pygame.time.Clock()
dt = clock.tick(600)


# pendulum parameters

MASS = 1
k = 0.00005
FRICTION = 0.00008
STEPS = 4

# magnet parameters
STRENGTH = 100
# initialize magnets
#for i in range(n):
#    magnets.append(Magnet(random.randint(0,WIDTH), random.randint(0,HEIGHT), 500))
    #magnets.append(Magnet(WIDTH//2+100, HEIGHT//2+100, 500))

for i in range(n):
    magnets.append(Magnet(random.randint(0,WIDTH), random.randint(0,HEIGHT), STRENGTH))

        # always add a magnet at the middle
magnets.append(Magnet(WIDTH/2, HEIGHT/2, STRENGTH))
done = False
while not done:
        if isFractalMode:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    pend = Pendulum(j, i, MASS, k, FRICTION, STEPS)
                    isStation = False
                    while not isStation:
                        isStation = pend.update(WIDTH, HEIGHT, magnets, dt, isStation)
                        #if (not isStation):
                            #print("finished")

                        if isDisplayWhileGenerating:
                            screen.fill((255,255,255))
                            # draw magnets
                            if len(magnets)!=0:
                                for magnet in magnets:
                                    pygame.draw.circle(screen, magnet.colour, (int(magnet.x),int(magnet.y)),20)

                            # draw pendulum
                            pygame.draw.circle(screen, (0, 0, 0), (int(pend.x),int(pend.y)),10)



                            pygame.display.flip()
                    img.putpixel((j,i), pend.lastColour)
                    if ((j % 100)==0):
                        print("[" + str(j) + ", " + str(i))
            img.save("D:/Documents/PythonProjects/Magnetic Pendulum/images/" + str(float(statistics.mean(pend.lastColour))) + ".bmp")
            isFractalMode = False
            
            

        # only in normal mode
        else:

            for event in pygame.event.get():
                    # Pressing E enters fractal generator mode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                           print("entered fractal generator mode")
                           isFractalMode = True

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = event.pos
                        # left click sets pendulum position
                        if event.button == 1:
                            pend = Pendulum(mx, my, MASS, k, FRICTION, STEPS)
                        # right click creates pendulum at mouse
                        if event.button == 2:
                            magnets.append(Magnet(mx, my, STRENGTH))

                        if event.button == 3 and len(magnets) != 0:
                            magnets.pop()

                    
                    if event.type == pygame.QUIT:
                            done = True
            pend.update(WIDTH, HEIGHT, magnets, dt, isStationary)
                
            screen.fill((255,255,255))
            # draw magnets
            if len(magnets)!=0:
                for magnet in magnets:
                    pygame.draw.circle(screen, magnet.colour, (int(magnet.x),int(magnet.y)),20)

            # draw pendulum
            pygame.draw.circle(screen, (0, 0, 0), (int(pend.x),int(pend.y)),10)



            pygame.display.flip()

        # miscellaneous logging
        #with open("mlist.csv","a") as f:
        #    writer = csv.writer(f,delimiter=",")
        #    writer.writerow([clock.get_time(),pend.M_x])
