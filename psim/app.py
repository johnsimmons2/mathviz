import sys
import pygame as pg
import numpy as np
import psim as ps
from pygame import QUIT
from psim.inputhandler import InputEvent, handleInput
from psim.const import sysvals
from psim.viewframe import ViewFrame

class App:
    def __init__(self):
        pg.init()
        self.state = 0
        self.views: list[ViewFrame] = []
        self.handledEvents = []
    
    def update(self):
        stats = self.views[self.state].update()
        txt = f'[View: {self.get().label} FPS: {self.get().fps} {"PAUSED" if self.get().paused else ""} {self.state+1}/{len(self.views)}]'
        if stats != None:
            stats = stats[0]
            txt = txt + f'{stats}'
        ps.renderer.drawText(txt)
        pg.display.update()

    def addView(self, view):
        self.views.append(view)
    
    def get(self, indx = None) -> ViewFrame:
        if indx == None:
            return self.views[self.state]
        if indx >= 0 and indx < len(self.views):
            return self.views[indx]
        elif abs(indx) < len(self.views):
            return self.views[indx]
    
    def set_caption(self, cap):
        pg.display.set_caption(cap)

    def set(self, state):
        if state < 0 or state >= len(self.views):
            return
        if self.get(state):
            self.get().activate(False)
            self.state = state
        self.get().activate(True)

    def valid(self) -> bool:
        if len(self.views) > 0:
            return True

    def blank(self):
        self.views[self.state].display.fill((255, 255, 255))

def handleEvents(events: list, app: App):
    for event in events:
        ev = handleInput(event)
        if ev.key not in app.handledEvents:
            if ev.key == pg.K_RIGHT:
                app.set(app.state + 1)
                app.handledEvents.append(ev.key)
            elif ev.key == pg.K_LEFT:
                app.set(app.state - 1)
                app.handledEvents.append(ev.key)
            else:
                app.get().pushEvent(ev)
        else:
            app.handledEvents.remove(ev.key)

APP = App()

def addSimulation(sim):
    APP.addView(sim)
    sysvals.VIEW = APP.get()
    print('Added Simulation: ', sim.label)
    print(sysvals.VIEW)

def start():
    global sysvals, APP
    APP.set_caption('Particle Simulator')

    if APP.valid():
        while True:
            APP.blank()
            handleEvents(pg.event.get(), APP)
            APP.update()
            sysvals.SCREEN = APP.get().display
            sysvals.VIEW = APP.get()