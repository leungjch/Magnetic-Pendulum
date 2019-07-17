import pygame
import random
class Magnet:
    def __init__(self, initx, inity, strength):
        self.x = initx
        self.y = inity
        self.strength = strength

        # pastel
        self.colour = self.generatePastel()
        # regular random
        #self.colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        
    def update(self, screen):
        

        pygame.draw.circle(screen, self.colour, (self.x,self.y),20)

    def generatePastel(self):
        red = random.randint(0,255)
        green = random.randint(0,255)
        blue = random.randint(0,255)
        return (int((red+255)/2),int((green+255)/2),int((blue+255)/2))
