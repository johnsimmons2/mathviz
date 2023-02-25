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
        self.display = pg.display.set_mode((self.width, self.height))
        self.simulation = False
        self.label = "entitylist"
        self.paused = False
        self.fps = fps
        self._pausedfps = 60
        self._cachefps = self.fps

    def setEntities(self, ents):
        self.entities = ents
    
    def attach(self, to):
        self.entities = [to]
        self.simulation = True
        self.label = type(to).__name__

    def setFPS(self, fps):
        self.fps = fps
        self._cachefps = fps
    
    def addFPS(self, fps):
        if self.fps + fps > 144 or self.fps + fps < 0:
            return
        self.fps += fps
        self._cachefps += fps

    def pause(self):
        if self.simulation:
            self.paused = not self.paused
            for e in self.entities:
                e.debugmode = not e.debugmode
            if self.paused:
                self.fps = self._pausedfps
            else:
                self.fps = self._cachefps
            print(self._cachefps)

    def update(self):
        stats = []
        for entity in self.entities:
            if not self.paused:
                stat = entity.update()
                if stat != None:
                    stats.append(stat)
            entity.display()
        self.FPSClock.tick(self.fps)
        return stats if len(stats) > 0 else None

    def click(self, position, ext):
        if self.simulation:
            self.entities[0].clicked(position[0], position[1], ext)