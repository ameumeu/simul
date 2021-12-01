# Simple pygame program

# Import and initialize the pygame library
import numpy as np
import pygame
import random
import math
import time
from datetime import datetime

pygame.init()

# Time
t = 1.0
# Fast forward (in move)
ff = 10e9
# Gravitational constant (Wikipedia)
G=6.673e-11*ff
# Number of particles
num = 7
# Screen size
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200

#class Particle
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, mass=1, rad=10, vx=0.0, vy=0.0, ax=0.0, ay=0.0):
        super(Particle, self).__init__()
        self.mass = mass
        self.pos = np.array([float(x), float(y)])
        self.v = np.array([vx, vy])
        self.a = np.array([ax, ay])
        self.rad = 1.0
        self.surf = pygame.Surface((rad,rad))
        #.circle(screen, (255, 255, 255), (self.rad, self.rad), 75)
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.left=self.pos[0]
        self.rect.top = self.pos[1]
    
    def draw(self):
            # Draw a solid blue circle in the center
        screen.blit(self.surf, (self.pos[0]/2, self.pos[1]/2))

    def move(self):
        # Velocity diff
        self.v[0] = self.v[0] + t*self.a[0]
        self.v[1] = self.v[1] + t*self.a[1]
        # Position diff
        self.pos[0] = self.pos[0] + t*self.v[0]
        self.pos[1] = self.pos[1] + t*self.v[1]
        
        # Move rect
        self.rect.left=self.pos[0]
        self.rect.top = self.pos[1]
        # Handle out of map
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.v=np.array((0,0))
            self.a=np.array((0,0))
        if self.pos[0] > SCREEN_WIDTH:
            self.pos[0] = SCREEN_WIDTH
            self.v=np.array((0,0))
            self.a=np.array((0,0))
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.v=np.array((0,0))
            self.a=np.array((0,0))
        if self.pos[1] > SCREEN_HEIGHT:
            self.pos[1] = SCREEN_HEIGHT
            self.v=np.array((0,0))
            self.a=np.array((0,0))




# Random seed
random.seed(datetime.now())

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH/2, SCREEN_HEIGHT/2])

# SCREEN_WIDTH = SCREEN_WIDTH*2
# SCREEN_HEIGHT = SCREEN_HEIGHT*2

# Make particles
particles = pygame.sprite.Group()

for i in range(num):
    k = Particle(random.random()+random.randint(0, SCREEN_WIDTH+1), random.random()+random.randint(0, SCREEN_HEIGHT+1))
    particles.add(k)

# Run until the user asks to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((0,0,0))

    temp = []
    for particle in particles:
        print(particle.rect)
        print(f"pos: {particle.pos}\nv: {particle.v}\na: {particle.a}\n")
        a_x=0
        a_y=0
        
        for a_p in particles:
            if a_p == particle :
                continue
            # distance
            d=a_p.pos-particle.pos
            r=math.sqrt(d[0]**2+d[1]**2)

            if r < 10e-3:
                continue

            # Check +/-
            if particle.pos[0] < a_p.pos[0]:
                a_x = a_x + G*a_p.mass*abs(d[0])/r**3
            elif particle.pos[0] > a_p.pos[0]:
                a_x = a_x - G*a_p.mass*abs(d[0])/r**3

            if particle.pos[1] < a_p.pos[1]:
                a_y = a_y + G*a_p.mass*abs(d[1])/r**3
            elif particle.pos[1] > a_p.pos[1]:
                a_y = a_y - G*a_p.mass*abs(d[1])/r**3
            
            # Detect collision
            # if particle.rect.colliderect(a_p):
            #     particle.v = particle.v-2*a_p.mass*(a_p.v-particle.v)/(particle.mass+a_p.mass)
                # particle.v[0] = particle.v[0]+a_p.mass*(a_p.v[0]-particle.v[0])/(particle.mass+a_p.mass)
                # particle.v[1] = particle.v[1]+a_p.mass*(a_p.v[1]-particle.v[1])/(particle.mass+a_p.mass)
                # a_p.v[0] = a_p.v[0]+particle.mass*(particle.v[0]-a_p.v[0])/(particle.mass+a_p.mass)
                # a_p.v[1] = a_p.v[1]+particle.mass*(particle.v[1]-a_p.v[1])/(particle.mass+a_p.mass)
                #print("collision:",particle.rect)

        # Give acceleration
        temp.append(np.array((a_x, a_y)))

    # Move
    i=0
    for particle in particles:
        particle.a = temp[i]
        particle.move()
        i = i+1
        particle.draw()

    #time.sleep(0.1)
    # Flip the display
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()