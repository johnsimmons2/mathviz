from psim.viewframe import ViewFrame
import pygame as pg
import sys

CLICK_DOWN = False
pts = []

def handleInput(event, viewFrame: ViewFrame, state):
    global CLICK_DOWN
    global pts
    if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
        pg.quit()
        sys.exit()
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_SPACE:
            viewFrame.pause()
        elif event.key == pg.K_UP:
            viewFrame.addFPS(1)
        elif event.key == pg.K_DOWN:
            viewFrame.addFPS(-1)
    elif event.type == pg.MOUSEBUTTONDOWN:
        CLICK_DOWN = True
        mx, my = pg.mouse.get_pos()
        ext = False
        if event.button == pg.BUTTON_LEFT:
            ext = True
        elif event.button == pg.BUTTON_MIDDLE:
            return not state
        viewFrame.click((mx, my), ext)
    elif event.type == pg.MOUSEMOTION:
        if CLICK_DOWN:
            mx, my = pg.mouse.get_pos()
            if (mx, my) not in pts:
                pts.append((mx, my))
                ext = False
                if pg.mouse.get_pressed() == (1, 0, 0):
                    ext = True
                viewFrame.click((mx, my), ext)
    elif event.type == pg.MOUSEBUTTONUP:
        CLICK_DOWN = False
    return state

