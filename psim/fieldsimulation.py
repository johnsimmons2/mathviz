from psim.entity import Entity
from psim.math import Vector2D, Field, VectorPairList
import psim as ps
import math
import numpy as np
import pygame as pg

class Fieldling:
    def __init__(self, index=0, pos=None, vel=None):
        self.index = index
        self.position = pos
        self.velocity = vel
        self.alive = False
        self.updates = 0
        self.aliveneighbors = 0
    
    def flip(self):
        self.alive = not self.alive
        self.updates += 1

    def die(self):
        self.alive = False
        self.updates += 1

    def birth(self):
        self.alive = True
        self.updates += 1

    def getAliveNeighbors(self, curIndex, field):
        toCheck = field.getNeighborIndices(curIndex)
        numAlive = 0
        for p in toCheck:
            if field[p].alive:
                numAlive += 1
        return numAlive

    @classmethod
    def tryRule(cls, point, numAlive, updates):
        if point.updates < updates:
            return cls.conway(point, numAlive)
        return point
    
    @classmethod
    def conway(self, point, numAlive):
        if point.alive:
            if numAlive <= 1:
                point.die()
            elif numAlive >= 4:
                point.die()
        else:
            if numAlive == 3:
                point.birth()
        return point

class ParticleField(Field):
    def __init__(self, resolution):
        super().__init__(ps.getDims(), resolution)
        for i in range(self._field_size):
            self._field[i] = Fieldling(i, self.getCoordsAt(i), Vector2D(np.random.rand()*255, np.random.rand()*255))

class FieldSimulation(Entity):
    def __init__(self, resolution=5):
        super().__init__(0, 0)
        self.resolution = resolution
        self.vecfield = ParticleField(resolution)
        self._debugmode = False
        self.paused = False
        self.updates = 0
    
    def pause(self):
        if self.paused:
            self.paused = False
            self._debugmode = False
        else:
            self.paused = True
            self._debugmode = True

    # !Overriding Entity! #
    def display(self):
        color = [0, 0, 0]
        wth = self.resolution
        for i, point in self.vecfield.get():
            if isinstance(point, Fieldling):
                color[0] = min((255 / 9) * point.aliveneighbors, 255)
                color[1] = 128 if point.alive else 0
                color[2] = 0 # min(point.velocity.magnitude(), 255)
                pt = point.position
                dx = (pt[0]*wth)
                dy = (pt[1]*wth)
                pg.draw.rect(ps.getScreen(), tuple(color), pg.rect.Rect(dx, dy, wth, wth))
                if self._debugmode:
                    txt = ps.getView().font.render(f'{pt}', True, (255,0,0))
                    ofsx = (wth/2) - txt.get_rect().width/2
                    ofsy = (wth/2) - txt.get_rect().height/2
                    ps.getScreen().blit(txt, (dx+ofsx, dy+ofsy))

    # !Overriding Entity! #
    def update(self):
        if not self.paused:
            for i, point in self.vecfield.get():
                if isinstance(point, Fieldling):
                    point.aliveneighbors = point.getAliveNeighbors(i, self.vecfield)
                    point = self.tryRule(point, point.aliveneighbors)
        self.updates += 1
    
    def tryRule(self, point, numAlive):
        return Fieldling.tryRule(point, numAlive, self.updates)
            
    def clicked(self, dx, dy):
        i = self.vecfield.valueAt(Vector2D(dx, dy))
        self.vecfield[i[0]].flip()

