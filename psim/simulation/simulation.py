from psim.particle import EParticleType
from psim.math import Vector2D, Vector2DRot
from psim.entity import Entity
import psim as ps
import numpy as np
import pygame as pg
import math

from psim.viewframe import ViewFrame


# TODO:
# - Saving and loading start parameters
# - Saving data and results
# - Change manner of rendering on the fly
class Simulation(ViewFrame):
    def __init__(self, width = None, height = None, fps = 144):
        super().__init__(width, height, fps)
