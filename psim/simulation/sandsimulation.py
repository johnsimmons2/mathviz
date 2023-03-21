from abc import abstractmethod
from psim.inputhandler import InputEvent, isClickDown
from psim.math import Field, Vector2D
from psim.simulation.simulation import Simulation
from enum import Enum
import numpy as np
import pygame as pg
import psim as ps


class EBlockType(Enum):
    NONE = 0,
    SAND = 1,
    WATER = 2

RULES = {
            EBlockType.NONE: {'solid': False, 'mass': 0.0, 'color': 'white'},
            EBlockType.SAND: {'solid': True, 'mass': 1.0, 'color': 'yellow'},
            EBlockType.WATER: {'solid': True, 'mass': 1.0, 'color': 'blue'}
        }


class Block:
    def __init__(self, pos, indx = 0, res = 0, type = EBlockType.NONE, ups = 0):
        self.index = indx
        self.resolution = res
        self.position = pos

        self.mass = RULES[type]['mass']
        self.solid = RULES[type]['solid']
        self.surfacetension = 0
        self.type = type
        self.updates = ups
    
    def __str__(self):
        return f"{self.index}\t{self.position}\t{self.updates}\n"

    def resetUpdates(self):
        self.updates = 0
        return self
    
    def setType(self, type):
        result = Block(self.position, self.index, self.resolution, type, self.updates)
        self.position = result.position
        self.solid = result.solid
        self.index = result.index
        self.resolution = result.resolution
        self.mass = result.mass
        self.updates = result.updates
        self.type = result.type
        return result

    def get_color(self):
        # colors = {EBlockType.NONE: [255, 255, 255], EBlockType.SAND: [170, 80, 20]}
        color = RULES[self.type]['color']
        return color

    def display(self):
        ps.renderer.drawRect(Vector2D(self.position[0] * self.resolution, self.position[1] * self.resolution), width=self.resolution, color=self.get_color(), debug=ps.sysvals.VIEW.debugmode)
       
    def clicked(self, ext):
        self.setType(ext)
            
class BlockField(Field):
    def __init__(self, resolution):
        super().__init__(ps.sysvals.getDims(), resolution)
        for i in range(self._field_size):
            self._field[i] = Block(self.getCoordsAt(i), i, resolution)

class SandSimulation(Simulation):
    def __init__(self, resolution):
        super().__init__()
        self.setUpdateRate(0.005)
        self.setFPS(60)
        self.resolution = resolution
        self.vecfield = BlockField(resolution)
        self.entities = self.vecfield._field
        self.label = 'Sand Simulation'
        self.paused = False
        self.updates = 0
        self.baseRules = [self.r_floor, self.r_updates]
        self.rules = {
            EBlockType.NONE: {'solid': False, 'mass': 0.0, 'color': 'white'},
            EBlockType.SAND: {'solid': True, 'mass': 1.0, 'color': 'yellow', 'rules': [self.r_solid_fall]},
            EBlockType.WATER: {'solid': True, 'mass': 1.0, 'color': 'blue', 'rules': [self.r_solid_fall]}
        }
    
    def _inner_display(self):
        self.label = f"Sand Simulation: Cursor [{self.cursorSize}/{self.cursorMaxSize}]"

    def _inner_update(self):
        self.vecfield._field = list(map(lambda x : x.resetUpdates(), self.vecfield._field))
        for i, n in self.vecfield.get():
            if isinstance(n, Block):
                if n.type == EBlockType.SAND:
                    for rule in self.baseRules:
                        if not rule(n):
                            break
                    for rule in self.rules[n.type]['rules']:
                        if not rule(n):
                            break

                    
        self.entities = self.vecfield._field

    def _update(self, index):
        self.vecfield._field[index].updates += 1

    def swap(self, indx1, indx2):
        self._update(indx1)
        self._update(indx2)
        self.vecfield.set(indx2, self.vecfield[indx2].setType(self.vecfield[indx1].type))
        self.vecfield.set(indx1, self.vecfield[indx1].setType(EBlockType.NONE))

    def _handleInputEvents(self):
        super()._cursorEventCheck()
        super()._baseEventCheck()
        for e in self._events:
            match(e):
                case InputEvent.MOUSE_CLICK_LEFT:
                    mx, my = pg.mouse.get_pos()
                    self.clicked(mx, my, EBlockType.WATER)
                    continue
                case InputEvent.MOUSE_CLICK_RIGHT:
                    mx, my = pg.mouse.get_pos()
                    self.clicked(mx, my, EBlockType.NONE)
                    continue
                case InputEvent.MOUSE_MOVE:
                    if isClickDown():
                        mx, my = pg.mouse.get_pos()
                        self.clicked(mx, my, EBlockType.SAND)
                        continue
        self._events = []
    
    def _base_rule(self, *block: Block):
        neighborhood = []
        for b in block:
            neighs = self.vecfield.getNeighborIndices(b.index)
            for n in neighs:
                neighborhood.append(self.vecfield.get(n))
        return neighborhood

    def r_solid_fall(self, block: Block):
        neigh = self._base_rule(block)
        for b in neigh:
            if b[1].position[1] > block.position[1]:
                if block.solid and not b[1].solid:
                    if block.updates != 1 and b[1].updates != 1:
                        self.swap(block.index, b[1].index)
                        return

    def r_water(self, block: Block):
        neigh = self._base_rule(block)
        for b in neigh:
            if b[1].position[0] == block.position[0]:
                if block.solid and not b[1].solid:
                    if block.updates != 1 and b[1].updates != 1:
                        self.swap(block.index, b[1].index)
                        return

    def r_floor(self, block: Block):
        if block.position[1] >= self.vecfield._adj_dims[1]:
            return False
        return True
        
    def r_updates(self, block: Block):
        if block.updates >= 1:
            return False
        return True