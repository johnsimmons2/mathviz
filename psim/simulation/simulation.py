from abc import abstractmethod
from psim.inputhandler import InputEvent
from psim.particle import EParticleType
from psim.math import Vector2D, Vector2DRot
from psim.entity import Entity
from psim.viewframe import ViewFrame
import psim as ps
import numpy as np
import pygame as pg
import math


# TODO:
# - Saving and loading start parameters
# - Saving data and results
# - Change manner of rendering on the fly
class Simulation(ViewFrame):
    def __init__(self, width = None, height = None, fps = 144):
        super().__init__(width, height, fps)
        self.vecfield = None
        self.resolution = None
        self.cursorSize = 1
        self.cursorMaxSize = 8

    def clicked(self, dx, dy, ext: bool):
        if self.resolution and self.vecfield:
            v = self.resolution
            clickLoc = self.vecfield.valueAt(Vector2D(dx, dy))
            if clickLoc and clickLoc[0]:
                self.vecfield[clickLoc[0]].clicked(ext)
                for n in range(self.cursorSize-1):
                    j = n * v
                    self.clickneighbor(ext, self.vecfield.valueAt(Vector2D(dx, dy)))
                    self.clickneighbor(ext, self.vecfield.valueAt(Vector2D(dx, dy+j)))
                    self.clickneighbor(ext, self.vecfield.valueAt(Vector2D(dx+j, dy)))
                    self.clickneighbor(ext, self.vecfield.valueAt(Vector2D(dx-j, dy-j)))
                    self.clickneighbor(ext, self.vecfield.valueAt(Vector2D(dx-j, dy+j)))
                    self.clickneighbor(ext, self.vecfield.valueAt(Vector2D(dx+j, dy-j)))
                    self.clickneighbor(ext, self.vecfield.valueAt(Vector2D(dx-j, dy)))
                    self.clickneighbor(ext, self.vecfield.valueAt(Vector2D(dx, dy-j)))
                    self.clickneighbor(ext, self.vecfield.valueAt(Vector2D(dx+j, dy+j)))
        else:
            self.click_at(dx, dy, ext)

    def _cursorEventCheck(self):
        for e in self._events:
            match(e):
                case InputEvent.KEY_UP:
                    if self.cursorSize < self.cursorMaxSize:
                        self.cursorSize += 1
                    continue
                case InputEvent.KEY_DOWN:
                    if self.cursorSize > 1:
                        self.cursorSize -= 1
                    continue
                case InputEvent.KEY_SPACE:
                    self.pause()
                    continue

    def clickneighbor(self, ext, tup = None):
        if tup:
            neighbor = self.vecfield[tup[0]]
            if isinstance(neighbor, Entity):
                neighbor.clicked(ext)
                neighs = self.vecfield.getNeighborIndices(tup[0])
                for n in neighs:
                    self.vecfield[n].clicked(ext)
    
    @abstractmethod
    def click_at(self, dx, dy, ext):
        pass
