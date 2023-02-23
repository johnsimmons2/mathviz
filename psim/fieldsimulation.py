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
        self.delta = False
        self.updates = 0
    
    def die(self):
        self.delta = True

    def birth(self):
        self.delta = True

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
                color[0] = 0
                color[1] = 255 if point.alive else 0
                color[2] = min(point.velocity.magnitude(), 255)
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
                toCheck = self.vecfield.getNeighborIndices(i)
                numAlive = 0
                if point.delta:
                    point.alive = not point.alive
                    point.delta = False
                else:
                    for p in toCheck:
                        if self.vecfield[p].alive:
                            numAlive += 1
                    point = self.tryRule(point, numAlive)
    
    def tryRule(self, point, numAlive):
        if point.alive:
            if numAlive <= 1:
                point.die()
            elif numAlive >= 4:
                point.die()
        else:
            if numAlive == 3:
                point.birth()
            

    def clicked(self, dx, dy):
        i = self.vecfield.valueAt(Vector2D(dx, dy))
        print(i)
        self.vecfield[i[0]].alive = not self.vecfield[i[0]].alive

