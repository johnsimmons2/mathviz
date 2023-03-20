import sys
import pygame as pg
import numpy as np
import psim as ps
from pygame import QUIT
from psim.inputhandler import InputEvent, handleInput
from psim.const import VIEW, WIDTH, HEIGHT, SCREEN

class App:
    def __init__(self):
        pg.init()
        self.state = 0
        self.views = []
    
    def update(self):
        self.views[self.state].active = True
        stats = self.views[self.state].update()
        txt = f'[View: {self.get().label}]'
        if stats != None:
            stats = stats[0]
            txt = txt + f'{stats}'
        text = VIEW.font.render(txt, True, (0, 0, 0))
        SCREEN.blit(text, (5, ps.getDims()[1]-50))
        pg.display.update()

    def addView(self, view):
        self.views.append(view)
    
    def get(self, indx = None):
        if indx == None:
            return self.views[self.state]
        if indx >= 0 and indx < len(self.views):
            return self.views[indx]
        elif abs(indx) < len(self.views):
            return self.views[indx]
    
    def set_caption(self, cap):
        pg.display.set_caption(cap)

    def set(self, state):
        mdl = state % len(self.views)
        if self.get(state):
            self.get().activate(False)
            print(self.get().active, self.get().label)
            self.state = state
        elif self.get(mdl):
            self.get().activate(False)
            self.state = mdl
        self.get().activate(True)

    def valid(self):
        if len(self.views) > 0:
            return True

    def blank(self):
        self.views[self.state].display.fill((255, 255, 255))

def handleEvents(events: list, app: App):
    for event in events:
        ev = handleInput(event)
        if ev == InputEvent.KEY_RIGHT:
            app.set(app.state + 1)
        elif ev == InputEvent.KEY_LEFT:
            app.set(app.state - 1)
        app.get().pushEvent(ev)

APP = App()

def addSimulation(sim):
    global APP, VIEW
    APP.addView(sim)
    VIEW = APP.get()

def start():
    global SCREEN, APP, VIEW
    APP.set_caption('Particle Simulator')

    if APP.valid():
        while True:
            APP.update()
            handleEvents(pg.event.get(), APP)
            APP.blank()
            SCREEN = APP.get().display
            VIEW = APP.get()

def getScreen():
    global SCREEN
    return SCREEN

def getDims():
    global WIDTH, HEIGHT
    return (WIDTH, HEIGHT)

def getView():
    global VIEW
    return VIEW