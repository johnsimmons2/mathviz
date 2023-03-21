import psim as ps
import math
import pygame as pg
from psim.math import Vector2D


def _getColor(color):
    if color in ps.sysvals.COLORS:
        colVal = ps.sysvals.COLORS[color]
    elif color in ps.sysvals.SCHEME:
        colVal = ps.sysvals.SCHEME[color]
    else:
        if isinstance(color, tuple) and len(color) == 3:
            colVal = color
        else:
            colVal = ps.sysvals.COLORS['black'] # Default color in case of fault
    return colVal

def drawLine(position1: Vector2D, position2: Vector2D, color='black'):
    pg.draw.aaline(ps.sysvals.SCREEN, _getColor(color), position1, position2)
 
def drawCircle(position: Vector2D, radius=5, color='black'):
    pg.draw.circle(ps.sysvals.SCREEN, _getColor(color), position, radius, radius)

def drawText(text, coords=None, color='text'):
    if coords == None:
        coords = (5, ps.sysvals.getDims()[1]-50)
    text = ps.sysvals.VIEW.font.render(text, True, _getColor(color))
    ps.sysvals.SCREEN.blit(text, coords)

def drawRectRGB(position: Vector2D, r, g, b, width = 5, debug = False):
    if isinstance(position, tuple):
        position = Vector2D(dims=position)
    pg.draw.rect(ps.sysvals.getScreen(), (r, g, b), pg.rect.Rect(position.x, position.y, width, width))
    if debug:
        ofsx = (width/2)
        ofsy = (width/2)
        txtPos = (position.x+ofsx, position.y+ofsy)
        drawText(f'{position}', txtPos)

def drawRect(position: Vector2D, width = 5, color = 'black', debug = False):
    if isinstance(position, tuple):
        position = Vector2D(dims=position)
    pg.draw.rect(ps.sysvals.getScreen(), _getColor(color), pg.rect.Rect(position.x, position.y, width, width))
    if debug:
        ofsx = (width/2)
        ofsy = (width/2)
        txtPos = (position.x+ofsx, position.y+ofsy)
        drawText(f'{position}', txtPos)

def drawVector2D(position: Vector2D, direction: Vector2D | None = None, debug: bool = False, radius: int = 5, color='black', length=100):
    if debug and direction:
        velocity = position + (direction * length)
        vec = (direction * length)
        vec.x = max(15, vec.x)
        vec.y = max(15, vec.y)
        angle = math.atan2(velocity.y, velocity.x) # Angle between velocity and x-axis
        drawLine(position, velocity, color=ps.sysvals.SCHEME['debugline'])
        drawLine(position, Vector2D(velocity.x, position.y), color=ps.sysvals.SCHEME['xaxis'])
        drawLine(position, Vector2D(position.x, velocity.y), color=ps.sysvals.SCHEME['yaxis'])
    drawCircle(position, radius=radius, color=_getColor(color))