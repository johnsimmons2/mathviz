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
        self.active = False
        self._fpp = 1/(fps)
        self._cachedupdaterate = self._fpp
        self._pausedfps = 144
        self._cachefps = fps
        self._events = []
        self._dt = 0
        self._t = pg.time.get_ticks()/1000

    def pushEvent(self, event: InputEvent):
        self._events.append(event)

    def setEntities(self, ents):
        self.entities = ents

    def setFPS(self, fps):
        self.fps = fps
        self._cachefps = fps
    
    def activate(self, val):
        self.active = val
        self._t = pg.time.get_ticks()/1000.0
    
    def setUpdateRate(self, rate):
        self._fpp = rate
        self._cachedupdaterate = rate
    
    def addFPS(self, fps):
        if self.fps + fps > 144 or self.fps + fps < 0:
            return
        self.fps += fps
        self._cachefps += fps

    def pause(self):
        self.paused = not self.paused
        self._t = pg.time.get_ticks()/1000.0
        for e in self.entities:
            e.debugmode = not e.debugmode
        if self.paused:
            self.fps = self._pausedfps
            self._fpp = (1/self._pausedfps)
        else:
            self.fps = self._cachefps
            self._fpp = (self._cachedupdaterate)

    def update(self):
        stats = []
        if self.active:
            self._handleInputEvents()
            time = pg.time.get_ticks()/1000.0
            frametime = time - self._t
            self._dt += frametime
            self._t = time
            self._handleInputEvents()
            if not self.paused:
                if self._dt >= self._fpp:
                    stat = self._inner_update()
                    if stat != None:
                        stats.append(stat)
                    self._dt = 0.0

            for e in self.entities:
                e.display()
            self.FPSClock.tick(self.fps)
            self._inner_display()
            return stats if len(stats) > 0 else None
        else:
            self._t = pg.time.get_ticks()/1000.0
            return None
    
    def _draw_circle(self, color, position, size):
        pg.draw.circle(self.display, color, position, size, size)

    @abstractmethod
    def _handleInputEvents(self):
        pass
    
    @abstractmethod
    def _inner_update(self):
        pass
        
    @abstractmethod
    def _inner_display(self):
        pass