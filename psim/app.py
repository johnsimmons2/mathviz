import sys
import pygame as pg
import numpy as np
import psim as ps
from pygame import QUIT
from psim import simulation, fieldsimulation
from psim.viewframe import ViewFrame

HEIGHT = 1080
WIDTH = 1920
FPS = 120
VIEW = ViewFrame()
SCREEN = VIEW.display

def start():
    global SCREEN
    pg.init()

    vf1 = ViewFrame()
    vf2 = ViewFrame()
    pg.display.set_caption("MathViz")

    sim = ps.Simulation()
    fieldsim = ps.FieldSimulation(120)
    vf2.attach(fieldsim)
    vf2.setFPS(5)
    vf1.attach(sim)
    state = True
    views = [vf1, vf2]
    
    while True:
        if state:
            VIEW = views[0]
        else:
            VIEW = views[1]
        SCREEN = VIEW.display
        SCREEN.fill((255,255,255))
        stats = VIEW.update()
        displayStats(state, stats)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                fieldsim.pause()
            if event.type == pg.MOUSEBUTTONDOWN:
                mx, my = pg.mouse.get_pos()
                if state:
                    if event.button == pg.BUTTON_LEFT:
                        sim.clicked(mx, my, True)
                    elif event.button == pg.BUTTON_RIGHT:
                        sim.clicked(mx, my, False)
                else:
                    fieldsim.clicked(mx, my)
                if event.button == pg.BUTTON_MIDDLE:
                    state = not state

        pg.display.update()

def displayStats(state, stats):
    if stats != None:
        stats = stats[0]
        text = VIEW.font.render(f'[View: ({1 if state else 2})] {len(VIEW.entities)} Vm={"{:.2f}".format(stats[0])} VM={"{:.2f}".format(stats[1])} Va={"{:.2f}".format(stats[2])} AvgP=({"{:.2f}".format(stats[3])}, {"{:.2f}".format(stats[4])})', True, (0,0,0))
        SCREEN.blit(text, (5, ps.getDims()[1]-25))
    text = VIEW.font.render(f'{"{:.2f}".format(VIEW.FPSClock.get_fps())} FPS', True, (0, 0, 0))
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