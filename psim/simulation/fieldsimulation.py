from psim.entity import Entity
from psim.inputhandler import InputEvent, isClickDown
from psim.math import Vector2D, Field, VectorPairList
import psim as ps
import math
import numpy as np
import pygame as pg

from psim.simulation.simulation import Simulation

class Fieldling(Entity):
    def __init__(self, index=0, pos=None, vel=None, res=0):
        super().__init__(pos[0], pos[1])
        self.index = index
        self.position = pos
        self.velocity = vel
        self.resolution = res
        self.alive = False
        self.updates = 0
        self.aliveneighbors = 0
    
    def clicked(self, ext: bool):
        self.alive = ext
    
    def display(self):
        color = [0, 0, 0]
        wth = self.resolution
        color[1] = -1 * max(self.aliveneighbors*(255//9), 0) + 255
        color[2] = 0 if self.alive else 255
        color[0] = 0 if self.alive else 255 # min(point.velocity.magnitude(), 255)
        pt = self.position
        dx = (pt[0]*wth)
        dy = (pt[1]*wth)
        pg.draw.rect(ps.getScreen(), tuple(color), pg.rect.Rect(dx, dy, wth, wth))
        if self.debugmode:
            txt = ps.getView().font.render(f'{pt}', True, (255,0,0))
            ofsx = (wth/2) - txt.get_rect().width/2
            ofsy = (wth/2) - txt.get_rect().height/2
            txtPos = (dx+ofsx, dy+ofsy)
            ps.getScreen().blit(txt, txtPos)
    
    def flip(self):
        self.alive = not self.alive
        self.updates += 1

    def die(self):
        self.alive = False
        self.updates += 1

    def birth(self):
        self.alive = True
        self.updates += 1

    def getAliveNeighbors(self, curIndex, field: Field):
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
            self._field[i] = Fieldling(i, self.getCoordsAt(i), Vector2D(np.random.rand()*255, np.random.rand()*255), resolution)

class FieldSimulation(Simulation):
    def __init__(self, resolution=5):
        super().__init__()
        self.setUpdateRate(1/4)
        self.setFPS(8)
        self.resolution = resolution
        self.vecfield = ParticleField(resolution)
        self.entities = self.vecfield._field
        self.paused = False
        self.updates = 0
        self.label = "Field Simulation"
    
    def _handleInputEvents(self):
        super()._cursorEventCheck()
        for e in self._events:
            match(e):
                case InputEvent.MOUSE_CLICK_LEFT:
                    mx, my = pg.mouse.get_pos()
                    self.clicked(mx, my, True)
                    continue
                case InputEvent.MOUSE_CLICK_RIGHT:
                    mx, my = pg.mouse.get_pos()
                    self.clicked(mx, my, False)
                    continue
                case InputEvent.MOUSE_MOVE:
                    if isClickDown():
                        mx, my = pg.mouse.get_pos()
                        self.clicked(mx, my, True)
                        continue
        self._events = []

    def _inner_display(self):
        self.label = f"Field Simulation: Cursor [{self.cursorSize}/{self.cursorMaxSize}]"

    # !Overriding Entity! #
    def _inner_update(self):
        for i, point in self.vecfield.get():
            if isinstance(point, Fieldling):
                point = self.tryRule(i, point)
        self.entities = self.vecfield._field
        self.updates += 1
    
    def tryRule(self, i, point):
        return Fieldling.tryRule(point, point.getAliveNeighbors(i, self.vecfield), self.updates)
            

