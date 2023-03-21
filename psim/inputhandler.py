from enum import Enum
import pygame as pg
import sys

class InputEvent(Enum):
    MOUSE_WHEEL_UP = 0,
    MOUSE_WHEEL_DOWN = 1,
    MOUSE_CLICK_LEFT = 2,
    MOUSE_CLICK_RIGHT = 3,
    MOUSE_CLICK_MIDDLE = 4,
    CLICK_HELD = 5,
    KEY_SPACE = 6,
    KEY_ESC = 7,
    KEY_UP = 8,
    KEY_DOWN = 9,
    KEY_LEFT = 10,
    KEY_RIGHT = 11,
    KEY_PRESS = 12,
    KEY_RELEASE = 13,
    MOUSE_MOVE = 14,
    KEY_D = 15

CLICK_DOWN = False
pts = []

def isClickDown():
    global CLICK_DOWN
    return CLICK_DOWN

def handleInput(event):
    global CLICK_DOWN
    global pts
    eventType: InputEvent = None
    shouldQuit = False
    if event.type == pg.QUIT:
        eventType = InputEvent.KEY_ESC
        shouldQuit = True

    if event.type == pg.KEYDOWN:
        if event.key == pg.K_SPACE:
            eventType = InputEvent.KEY_SPACE
        elif event.key == pg.K_UP:
            eventType = InputEvent.KEY_UP
        elif event.key == pg.K_DOWN:
            eventType = InputEvent.KEY_DOWN
        elif event.key == pg.K_ESCAPE:
            eventType = InputEvent.KEY_ESC
            shouldQuit = True
        elif event.key == pg.K_LEFT:
            eventType = InputEvent.KEY_LEFT
        elif event.key == pg.K_RIGHT:
            eventType = InputEvent.KEY_RIGHT
        elif event.key == pg.K_d:
            eventType = InputEvent.KEY_D

    elif event.type == pg.MOUSEBUTTONDOWN:
        CLICK_DOWN = True
        mx, my = pg.mouse.get_pos()
        if event.button == pg.BUTTON_LEFT:
            eventType = InputEvent.MOUSE_CLICK_LEFT
        elif event.button == pg.BUTTON_RIGHT:
            eventType = InputEvent.MOUSE_CLICK_RIGHT
        elif event.button == pg.BUTTON_MIDDLE:
            eventType = InputEvent.MOUSE_CLICK_MIDDLE

    elif event.type == pg.MOUSEMOTION:
        eventType = InputEvent.MOUSE_MOVE
        if CLICK_DOWN:
            mx, my = pg.mouse.get_pos()
            if (mx, my) not in pts:
                pts.append((mx, my))
    elif event.type == pg.MOUSEBUTTONUP:
        CLICK_DOWN = False
    
    if shouldQuit:
        pg.quit()
        sys.exit()
    return eventType

