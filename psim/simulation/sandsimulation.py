from abc import abstractmethod
from psim.entity import Entity
from psim.math import Field, Vector2D
from psim.simulation.simulation import Simulation
from enum import Enum
import numpy as np
import pygame as pg
import psim as ps

class EBlockType(Enum):
    NONE = 0,
    AIR = 1,
    SAND = 2

class Block(Entity):
    def __init__(self, pos, indx = 0, res = 0):
        super().__init__(pos[0], pos[1])
        self.index = indx
        self.resolution = res
        self.position = pos
        self.type = EBlockType.NONE
    
    def getAbove(self):
        pass

    def getBelow(self):
        pass

    def getLeft(self):
        pass

    def getRight(self):
        pass

    def move(self, x, y):
        pass

    @abstractmethod
    def _inner_update(self):
        pass

    @abstractmethod
    def _get_color(self):
        pass

    def update(self):
        self._inner_update()

    def display(self):
        color = self._get_color()
        wth = self.resolution
        pt = self.position
        dx = (pt[0]*wth)
        dy = (pt[1]*wth)
        pg.draw.rect(ps.getScreen(), tuple(color), pg.rect.Rect(dx, dy, wth, wth))

class AirBlock(Block):
    def __init__(self, pos, indx, res):
        super().__init__(pos, indx, res)
    
    def _get_color(self):
        return [255, 255, 255]

class SandBlock(Block):
    def __init__(self, pos, indx, res):
        super().__init__(pos, indx, res)
    
    def _get_color(self):
        return [180, 20, 120]
    
    def _inner_update(self):
        neighbors = [self.getBelow()]
        for n in neighbors:
            if isinstance(n, Block):
                if n.type == EBlockType.AIR or n.type == EBlockType.NONE:
                    self.move(0, -1)

class ParticleField(Field):
    def __init__(self, resolution):
        super().__init__(ps.getDims(), resolution)
        for i in range(self._field_size):
            self._field[i] = Block(i, self.getCoordsAt(i), Vector2D(np.random.rand()*255, np.random.rand()*255), resolution)

class SandSimulation(Simulation):
    def __init__(self, resolution):
        super().__init__()
        self.resolution = resolution
        self.vecfield = 