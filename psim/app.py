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
    
    def set_caption(self, cap):
        pg.display.set_caption(cap)

    def set(self, state):
        if self.get(state):
            self.state = state
            return
    
    def blank(self):
        self.views[self.state].display.fill((255, 255, 255))


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
        for event in pg.event.get():
            ev=handleInput(event)
            if ev == InputEvent.KEY_RIGHT:
                curState = app.state
                if curState + 1 < len(app.views):
                    app.set(curState + 1)
            elif ev == InputEvent.KEY_LEFT:
                curState = app.state
                if curState - 1 >= 0:
                    app.set(curState - 1)
            else:
                if ev:
                    app.get().pushEvent(ev)


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