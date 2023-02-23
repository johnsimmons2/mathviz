from __future__ import annotations
from psim.entity import Entity
from psim.math import Vector2D, Vector2DRot
from enum import Enum
import math
import numpy as np
import pygame as pg
import psim as ps

DEBUG = True

class EParticleType(Enum):
    NONE = 0,
    RED = 1,
    BLUE = 2,
    GREEN = 3,
    PURPLE = 4

class Particle(Entity):
    def __init__(self, pos: Vector2D = None, vel: Vector2DRot = None, type: EParticleType = EParticleType.NONE, x = None, y = None):
        if pos == None:
            if x != None and y != None:
                self.position = Vector2D(x, y)
                super().__init__(x, y)
        else:
            super().__init__(pos.x, pos.y)
            self.position = pos
        self.type = type
        self.x = self.position.x
        self.y = self.position.y
        self.screen = ps.getScreen()
        self.r, self.g, self.b = 0, 0, 0

        self.dist = 0
        self.wavelength = 0
        self.mass = 1
        self.size = 5
        self.thickness = 5
        self.active = True
        self.flagged = True
        self.setColors()

        if vel != None:
            self.angle = vel.angle
            self.velocity = vel.magnitude()
        else:
            self.angle = np.random.random() * 2 * math.pi
            self.velocity = np.random.rand()

    def setColors(self):
        match(self.type):
            case EParticleType.NONE:
                self.r = 255
                self.g = 255
                self.b = 255
                return
            case EParticleType.RED:
                self.r = 255
                self.g = 0
                self.b = 0
                return
            case EParticleType.BLUE:
                self.r = 0
                self.g = 0
                self.b = 255
                return
            case EParticleType.GREEN:
                self.r = 0
                self.g = 255
                self.b = 0
                return
            case EParticleType.PURPLE:
                self.r = 255
                self.g = 0
                self.b = 255
                return

    def update(self):
        pass

    # !Overriding Entity! #
    def display(self):
        global DEBUG
        if DEBUG:
            leng = math.hypot(self.velocity * math.sin(self.angle), self.velocity * math.cos(self.angle))
            if leng > 1:
                pg.draw.aaline(self.screen, (255,0,0), (self.x, self.y), (20*self.velocity * math.sin(self.angle)+self.x, 20*self.velocity * math.cos(self.angle)+self.y))
            else:
                pg.draw.aaline(self.screen, (128, 128, 128), (self.x, self.y), (20*self.velocity * math.sin(self.angle)+self.x, 20*self.velocity * math.cos(self.angle)+self.y))
        pg.draw.circle(self.screen, (self.r, self.g, self.b), (self.x, self.y), self.size, self.thickness)

    def move(self):
        if abs(self.x) > 5000 or abs(self.y) > 5000:
            self.active = False
        if self.active:
            dx = math.sin(self.angle) * self.velocity
            dy = math.cos(self.angle) * self.velocity
            dist = math.hypot(dx, dy)
            exE = ps.SPEED_LIMIT - dist
            
            self.x += dx
            self.y -= dy

            # If you go over the speed limit
            if exE < 0:
                d2x = exE * math.sin(self.angle)
                d2y = exE * math.cos(self.angle)
                self.x -= d2x
                self.y -= d2y
                self.velocity += exE

    def collide(self, p: Particle):
        dx = self.x - p.x
        dy = self.y - p.y
        
        dist = math.hypot(dx, dy)
        if self.active == False or p.active == False:
            return None
        if dist < self.size + p.size:
            angle = math.atan2(dy, dx) + 0.5 * math.pi
            total_mass = self.mass + p.mass

            vec1 = addVectors((self.angle, self.velocity*(self.mass-p.mass)/total_mass), (angle, 2*p.velocity*p.mass/total_mass))
            vec2 = addVectors((p.angle, p.velocity*(p.mass-self.mass)/total_mass), (angle+math.pi, 2*self.velocity*self.mass/total_mass))

            self.accelerate(vec1)
            p.accelerate(vec2)

            overlap = 0.5*(self.size + p.size - dist+1)
            self.x += math.sin(angle)*overlap
            self.y -= math.cos(angle)*overlap
            p.x -= math.sin(angle)*overlap
            p.y += math.cos(angle)*overlap
    
    def photocollision(self, p: Particle):
        dx = self.x - p.x
        dy = self.y - p.y
        
        dist = math.hypot(dx, dy)
        if dist < self.size + p.size:
            self.active = False
            (p.angle, p.velocity) = addVectors((self.angle, self.velocity), (p.angle, p.velocity))
            p.velocity = p.velocity / 2

    def accelerate(self, vec):
        velE = ps.SPEED_LIMIT - vec[1]
        spd = ps.SPEED_LIMIT-ps.GRAV_CONST
        if velE < 0:
            (self.angle, self.velocity) = (vec[0], spd)
            return None
        (self.angle, self.velocity) = vec

    def gravity(self, other: Particle):
        dx = self.x - other.x
        dy = self.y - other.y
        dist  = math.hypot(dx, dy)
        
        if dist < self.size + other.size:
            return None
            
        theta = math.atan2(dy, dx)
        force =  ps.GRAV_CONST*other.mass*self.mass/(dist ** 2)
        vec1 = addVectors((self.angle, self.velocity), (theta - 0.5 * math.pi, force/self.mass))
        vec2 = addVectors((other.angle, other.velocity), (theta + 0.5 * math.pi, force/other.mass))
        # if self.velocity > 1:
            # print(f'{other.mass}*{self.mass}/{dist**2}=[{force}]\t{dx},{dy}|{dist}|{self.velocity}')
        return (self.accelerate(vec1), other.accelerate(vec2))


# Adds 2 vectors, vector elements are angle, speed.
def addVectors(vec1, vec2):
    x  = math.sin(vec1[0]) * vec1[1] + math.sin(vec2[0]) * vec2[1]
    y  = math.cos(vec1[0]) * vec1[1] + math.cos(vec2[0]) * vec2[1]

    angle  = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)
    # if length > 1:
    #     length = 1

    return (angle, length)