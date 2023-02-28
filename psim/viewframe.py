from abc import abstractmethod
import pygame as pg
from psim.entity import Entity
from psim.inputhandler import InputEvent


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
        self._events = []

    def pushEvent(self, event: InputEvent):
        self._events.append(event)

    def setEntities(self, ents):
        self.entities = ents

    def setFPS(self, fps):
        self.fps = fps
        self._cachefps = fps
    
    def addFPS(self, fps):
        if self.fps + fps > 144 or self.fps + fps < 0:
            return
        self.fps += fps
        self._cachefps += fps

    def pause(self):
        self.paused = not self.paused
        for e in self.entities:
            e.debugmode = not e.debugmode
        if self.paused:
            self.fps = self._pausedfps
        else:
            self.fps = self._cachefps

    def update(self):
        stats = []
        self._handleInputEvents()
        if not self.paused:
            stat = self._inner_update()
            if stat != None:
                stats.append(stat)
        for e in self.entities:
            e.display()
        self.FPSClock.tick(self.fps)
        return stats if len(stats) > 0 else None
    
    def _draw_circle(self, color, position, size):
        pg.draw.circle(self.display, color, position, size, size)

    @abstractmethod
    def _handleInputEvents(self):
        pass
    
    @abstractmethod
    def _inner_update(self):
        pass