import pygame as pg
from psim.entity import Entity


class ViewFrame:
    def __init__(self, width = None, height = None, fps = 144):
        pg.font.init()
        if width and height:
            self.width = width
            self.height = height
        else:
            self.width = 1920
            self.height = 1080
        self.FPSClock = pg.time.Clock()
        self.font = pg.font.Font('freesansbold.ttf', 16)
        self.entities: list[Entity] = []
        self.fps = fps
        self.display = pg.display.set_mode((self.width, self.height))

    def setEntities(self, ents):
        self.entities = ents
    
    def attach(self, to):
        self.entities = [to]

    def setFPS(self, fps):
        self.fps = fps

    def update(self):
        stats = []
        for entity in self.entities:
            stat = entity.update()
            if stat != None:
                stats.append(stat)
            entity.display()
        self.FPSClock.tick(self.fps)
        return stats if len(stats) > 0 else None