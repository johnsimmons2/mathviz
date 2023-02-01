# Prune chains during sleep
# Chemical signaling to other networks
# Periodic waves to add a temporal behavior
# Uncertainty / noise to all data


# Environment has criteria for survival

import math
import sys
import numpy as np
import matplotlib.pyplot as plt
import pygame as pg
from pygame import QUIT

HEIGHT = 720
WIDTH = 1080
SCREEN = None

# from unitons import Uniton, PRIMES, AMOUNT


# def getUnitons():
#     AMOUNT
#     nums = []
#     for i in range(AMOUNT):
#         nums.append(Uniton(i))
#     return nums

# UNITONS = getUnitons()

class Particle(pg.sprite.Sprite):
    def __init__(self, x, y):
        global WIDTH, HEIGHT, SCREEN
        super().__init__()
        self.x = x
        self.y = y
        self.r = 0
        self.g = 255
        self.b = 0
        self.size = 15
        self.thickness = 15
        self.screen = SCREEN
        self.angle = np.random.random() * 2 * math.pi
        self.angularacc = 0
        self.velocity = np.random.random() * 1.5
        self.active = True

    def display(self):
        if self.active:
            pg.draw.circle(self.screen, (self.r, self.g, self.b), (self.x, self.y), self.size, self.thickness)

    def move(self):
        if self.active:
            global WIDTH, HEIGHT
            movX = self.x + math.sin(self.angle) * self.velocity
            movY = self.y + math.cos(self.angle) * self.velocity

            if movX + self.size > WIDTH:
                movX = 2 * (WIDTH - self.size) - movX
                self.angle = -self.angle
            elif movX < self.size:
                movX = 2 * self.size - movX
                self.angle = -self.angle

            if movY + self.size > HEIGHT:
                movY = 2 * (HEIGHT - self.size) - movY
                self.angle = math.pi - self.angle
            elif movY < self.size:
                movY = 2 * self.size - movY
                self.angle = math.pi - self.angle

                
            self.y = movY
            self.x = movX
            self.angle = self.angle + self.angularacc
            self.b = min(abs(self.angularacc * 200), 255)

    def collide(p1, p2):
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        d = math.hypot(dx, dy)
        # Amount of overlap to quantify energy of collision?
        if d < p1.size + p2.size:
            power = math.cos(p1.angle - p2.angle)
            if abs(power) >= 0.95:
                if power > 0:
                    dpower = 1 - power
                else:
                    dpower = 1 + power * -1

                if p1.velocity > p2.velocity:
                    p2.active = False
                    p1.angularacc = p1.angularacc + dpower
                    p1.r = min(p1.r + 10, 255)
                    p1.g = max(p1.g - 10, 0)
                    p1.velocity = p2.velocity * abs(power)
                elif p2.velocity > p1.velocity:
                    p1.active = False
                    p2.angularacc = p2.angularacc + dpower
                    p2.g = max(p2.g - 10, 0)
                    p2.r = min(p2.r + 10, 255)
                    p2.velocity = p2.velocity * abs(power)

            tangent = math.atan2(dy, dx)
            angle = 0.5 * math.pi + tangent

            angle1 = 2*tangent - p1.angle
            angle2 = 2*tangent - p2.angle

            (p1.angle, p1.velocity) = (angle1, p2.velocity)
            (p2.angle, p2.velocity) = (angle2, p1.velocity)

            p1.x += math.sin(angle)
            p1.y -= math.cos(angle)
            p2.x -= math.sin(angle)
            p2.y += math.cos(angle)

            # How much it bounces contrary to the angular momentum angle should be how it slows down this momentum or imparts it elsewhere
            p1.angularacc = (p1.angularacc + p2.angularacc)/2
            p2.angularacc = (p1.angularacc + p2.angularacc)/2


def makeParticles():
    prts = []
    for i in range(100):
        prts.append(Particle(np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT)))
    return prts

def main():
    pg.init()
    global WIDTH, HEIGHT, SCREEN
    vec = pg.math.Vector2
    FPS = 120
    FPSClock = pg.time.Clock()

    display = pg.display.set_mode((WIDTH, HEIGHT))
    SCREEN = display
    pg.display.set_caption("Simulation")

    particles = makeParticles()

    while True:
        display.fill((255,255,255))
        for i, e in enumerate(particles):
            if not e.active:
                continue
            e.display()
            e.move()
            for p in particles[i+1:]:
                Particle.collide(e, p)
        pg.display.update()

        FPSClock.tick()
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()


if __name__ == "__main__":
    main()