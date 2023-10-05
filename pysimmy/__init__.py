import pygame as pg
from pysimmy.View import View
from pysimmy.Datalayer import DataCache, getDataLayer

class App:
    def __init__(self, width, height, fps):
        pg.init()
        pg.font.init()
        self.clock = pg.time.Clock()
        self.width = width
        self.height = height
        self.fps = fps
        self.running = True
        self.simulations = []
    
    def addSimulation(self, sim):
        self.simulations.append(sim)

    def loop(self):
        for s in self.simulations:
            self.clock.tick(self.fps)
            s.view.display.fill('white')
            s.draw()
            s.update()
            self.handleEvents(pg.event.get())
            pg.display.flip()

    def handleEvents(self, events: list):
        for event in events:
            print(event)

    def start(self):
        if self.simulations == None or len(self.simulations) == 0:
            raise Exception('No simulations added to App')
        while self.running:
            self.loop()
        pg.quit()