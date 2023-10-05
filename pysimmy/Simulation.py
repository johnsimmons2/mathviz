from abc import abstractmethod
import pygame as pg
from pysimmy.Datalayer import getDataLayer
from pysimmy.View import ParticleVC

class Simulator:
    def __init__(self, view, datalayerid):
        self.view = view
        self.datalayerid = datalayerid
        self.viewchild = None

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass

class ParticleSimulator(Simulator):
    def __init__(self, view, datalayerid):
        super().__init__(view, datalayerid)
        self.particles = []
        self.viewchild = ParticleVC()

    def update(self):
        cache = getDataLayer().getCache(self.datalayerid)
        if cache:
            for d in cache.data:
                if 'y' in d and 'x' in d:
                    d['x'] += 1
    
    def draw(self):
        cache = getDataLayer().getCache(self.datalayerid)
        if cache:
            for d in cache.data:
                if 'y' in d and 'x' in d:
                    pg.draw.circle(self.view.display, (0, 0, 0), (d['x'], d['y']), 5)