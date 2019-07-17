import pygame
import math
class Pendulum:
    def __init__(self, initx, inity, mass, k, friction, STEPS):

        # position
        self.x = initx
        self.y = inity
        self.mass = mass

        # acceleration
        self.a_x = 0
        self.a_y = 0
        
        # velocity
        self.v_x = 0
        self.v_y = 0
        
        # Tension force
        self.T_x = 0
        self.T_y = 0 
        self.k = k
        # Friction coefficient
        self.friction = friction

        # Magnetic force
        self.M_x = 0
        self.M_y = 0

        # Net force
        self.Fnet_x = 0
        self.Fnet_y = 0

        # For Euler integration
        self.steps = STEPS;
        self.delta = 1/STEPS

        # Misc
        self.lastColour = (0,0,0) # Colour of the last magnet it was pulled into
        self.xlist = []
        self.ylist = []

    def update(self, WIDTH, HEIGHT, magnets, dt, isStationary):

        #width, height = pygame.display.get_surface().get_size() # Get screen heigth and width
        #width, height = pygame.display.get_surface().get_size() # Get screen heigth and width
        width = WIDTH
        height = HEIGHT
        # Calculate tension (Hookes law: F_T = kx where x is distance from center)
        self.T_x = self.k * (width/2-self.x)
        self.T_y = self.k * (height/2-self.y)

        # Calculate net magnetic force
        self.M_x = 0
        self.M_y = 0
        if len(magnets) != 0:
            for magnet in magnets:
                #print("diff y is : " + str(abs(magnet.y - self.y)))
                #print("diff x is : " + str(abs(magnet.x - self.x)))
                
                if math.sqrt(((magnet.x - self.x)**2)+((magnet.y - self.y)**2)) >= 15:
                    try:
                        M = math.sqrt((magnet.x - self.x)**2+(magnet.y - self.y)**2)
                        self.M_x += magnet.strength * (magnet.x - self.x)/(M**3)
                        self.M_y += magnet.strength * (magnet.y - self.y)/(M**3)
                    except OverflowError:
                        print("oops")
                        print(magnet.x - self.x)
                        print(magnet.y - self.y)
                        print(M)

                # if it is pulled into the magnet
                else:

                    self.x = magnet.x
                    self.y = magnet.y
                    isStationary = True
                    self.lastColour = magnet.colour
                    #print(self.lastColour)

                    break
        # Calculate net force
        self.Fnet_x = self.T_x + self.M_x
        self.Fnet_y = self.T_y + self.M_y 

        # Calculate acceleration (Fnet=ma)
        self.a_x = self.Fnet_x/self.mass 
        self.a_y = self.Fnet_y/self.mass 

        # Apply friction
        self.a_x -= self.v_x * self.friction
        self.a_y -= self.v_y * self.friction

        # Euler integration
        for i in range(self.steps):
            self.v_x += self.a_x*self.delta        
            self.v_y += self.a_y*self.delta
            
    
            
            self.x += self.v_x *self.delta
            self.y += self.v_y *self.delta 


        
        #print("v" + str(self.v_x))
        #print("Fnet" + str(self.Fnet_x))
        #print("T" + str(self.T_x))
        #print("M" + str(self.M_x))
        #print("A" + str(self.a_x))
        #print("S" + str(self.x))
        #print(self.x)
        #if abs(self.Fnet_x) > 1:
        #    print("here")
        #self.xlist.append(self.x)
        #self.ylist.append(self.y)
        return isStationary
        #for i in range(len(self.xlist)):
        #    screen.set_at((int(self.xlist[i]), int(self.ylist[i])), (0,0,0))

    
