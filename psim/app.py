import sys
import pygame as pg
import numpy as np
import psim as ps
from pygame import QUIT
from psim.simulation import ParticleSimulation, FieldSimulation
from psim.viewframe import ViewFrame
from psim.inputhandler import InputEvent, handleInput

HEIGHT = 1080
WIDTH = 1920
FPS = 120
VIEW = ViewFrame()
SCREEN = VIEW.display

class App:
    def __init__(self):
        pg.init()
        self.state = 0
        self.views: ViewFrame = []
    
    def update(self):
        self.views[self.state].update()
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
        else: print(indx)
    
    def set_caption(self, cap):
        pg.display.set_caption(cap)

    def set(self, state):
        mdl = state % len(self.views)
        if self.get(state):
            self.state = state
        elif self.get(mdl):
            self.state = mdl

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


def start():
    global SCREEN
    app = App()
    app.set_caption('Particle Simulator')

    sim = ParticleSimulation(50)
    fieldsim = FieldSimulation(10)
    app.addView(sim)
    app.addView(fieldsim)
    
    while True:
        stats = app.update()
        app.blank()
        displayStats(app, stats)
        handleEvents(pg.event.get(), app)


def displayStats(app, stats):
    txt = f'[View: {app.get().label}]'
    if stats != None:
        stats = stats[0]
        txt = txt + f'{stats}'
    text = VIEW.font.render(txt, True, (0, 0, 0))
    SCREEN.blit(text, (5, ps.getDims()[1]-50))

def getScreen():
    global SCREEN
    return SCREEN

def getDims():
    global WIDTH, HEIGHT
    return (WIDTH, HEIGHT)

def getView():
    global VIEW
    return VIEW