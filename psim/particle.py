from __future__ import annotations
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

class Particle:
    def __init__(self, pos: Vector2D = None, vel: Vector2DRot = None, type: EParticleType = EParticleType.NONE, x = None, y = None):
        if pos == None:
            if x != None and y != None:
                self.position = Vector2D(x, y)
            else:
                self.position = Vector2D(np.random.rand() * 1920, np.random.rand() * 1080)
        else:
            self.position = pos
        self.type = type
        self.x = self.position.x
        self.y = self.position.y
        self.screen = ps.sysvals.getScreen()
        self.color = self.setColors()

        self.dist = 0
        self.wavelength = 0
        self.mass = 1
        self.size = 5
        self.thickness = 5
        self.active = True
        self.flagged = True
        
        self.gravityvec = Vector2DRot(0, 0)
        if type == EParticleType.RED:
            self.mass = 500
        if vel != None:
            self.angle = vel.angle
            self.velocity = vel.magnitude()
        else:
            self.angle = np.random.random() * 2 * math.pi
            self.velocity = np.random.rand()

    def setColors(self):
        match(self.type):
            case EParticleType.NONE:
                return ps.sysvals.COLORS['black']
            case EParticleType.RED:
                return ps.sysvals.COLORS['red']
            case EParticleType.BLUE:
                return ps.sysvals.COLORS['blue']
            case EParticleType.GREEN:
                return ps.sysvals.COLORS['green']
            case EParticleType.PURPLE:
                return ps.sysvals.COLORS['purple']

    def update(self):
        pass

    def display(self):
        ps.renderer.drawVector2D(self.position, self.getDirection(), ps.sysvals.VIEW.debugmode, color=self.color)

    def getDirection(self):
        return Vector2D(self.velocity * math.sin(self.angle), self.velocity * math.cos(self.angle))

    def move(self):
        if abs(self.x) > 5000 or abs(self.y) > 5000:
            self.active = False
        if self.active:
            gx = math.sin(self.gravityvec.angle) * self.gravityvec.dist
            gy = math.cos(self.gravityvec.angle) * self.gravityvec.dist
            self.angle += (self.gravityvec.angle * self.gravityvec.dist)/(self.velocity + 1)
            dx = math.sin(self.angle) * self.velocity
            dy = math.cos(self.angle) * self.velocity
            self.position = self.position + (dx + gx, dy + gy)

    def collide(self, p: Particle):
        dx = (self.position - p.position).x
        dy = (self.position - p.position).y
        
        dist = math.hypot(dx, dy)
        if self.active == False or p.active == False:
            return None
        if dist < self.size + p.size:
            angle = math.atan2(dy, dx) + 0.5 * math.pi

            self.angle = angle
            p.angle = angle - math.pi/2

            vel1 = p.velocity
            vel2 = self.velocity

            self.velocity = vel1
            p.velocity = vel2

            overlap = 0.5*(self.size + p.size)

            self.position = self.position + (math.sin(angle)*overlap, math.cos(angle)*overlap)
            p.position = p.position + (math.sin(angle - math.pi/2)*overlap, math.cos(angle - math.pi/2)*overlap)
    
    def gravity(self, other: Particle):
        dx = self.position.x - other.position.x
        dy = self.position.y - other.position.y
        dist = math.hypot(dx, dy)
        
        if dist < self.size + other.size:
            return None
        
        theta = math.atan2(dy, dx)
        force = 0.25 * other.mass*self.mass/(dist ** 2)
        self.gravityvec = Vector2DRot(force/self.mass, math.pi + theta)
        other.gravityvec = Vector2DRot(force/other.mass, math.pi - theta)


# Adds 2 vectors, vector elements are angle, speed.