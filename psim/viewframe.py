import pygame as pg
from psim.entity import Entity


class ViewFrame:
    def __init__(self, width = None, height = None, fps = 144):
        pg.font.init()
        if width and height:
            self.FPSClock = pg.time.Clock()
            self.font = pg.font.Font('freesansbold.ttf', 16)
            self.entities: list[Entity] = []
        else:
            width = 1920
            height = 1080
            self.FPSClock = pg.time.Clock()
            self.font = pg.font.Font('freesansbold.ttf', 16)
            self.entities: list[Entity] = []
        self.fps = fps
        self.display = pg.display.set_mode((width, height))

    def setEntities(self, ents):
        self.entities = ents
    
    def attach(self, to):
        self.entities = [to]

    def setFPS(self, fps):
        self.fps = fps

    def update(self):
        for entity in self.entities:
            entity.update()
            entity.display()
            self.FPSClock.tick(self.fps)