import numpy as np
import pygame as pg
from psim.entity import Entity

class Field(Entity):
    def __init__(self, dims: tuple, resolution: int):
        self.dimensions = dims
        self.resolution = resolution
        self.field = np.zeros(dims)
        self.entities = []
    
    def populate(self, entity: Entity):
        px, py = entity.getPosition()//self.resolution
        self.field[px][py]
        self.entities.append(entity)
    
    def display(self):
        pg.draw.circle()