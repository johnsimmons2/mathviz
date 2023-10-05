from abc import abstractmethod
import pygame as pg

class ViewChild:
    def __init__(self):
        pass

    @abstractmethod
    def draw(self):
        pass

class ParticleVC(ViewChild):
    def __init__(self):
        pass

class View:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        self.FPSClock = pg.time.Clock()
        self.font = pg.font.Font('freesansbold.ttf', 16)
        self.display = pg.display.set_mode((self.width, self.height))
        self.label = "No Label"
        self.paused = False
        self.active = False

        self._viewchildren: list[ViewChild] = []

        self._dt = 0
        self._t = pg.time.get_ticks()/1000