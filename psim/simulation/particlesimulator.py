from psim.inputhandler import InputEvent
from psim.math import Field, Vector2D
from psim.particle import EParticleType, Particle
from psim.simulation.simulation import Simulation
import pygame as pg
import math
import psim as ps

class ParticleSimulation(Simulation):
    def __init__(self, numParticles):
        super().__init__()
        self.entities: list[Particle] = [Particle(type=EParticleType.BLUE) for _ in range(numParticles)]
        self.label = "Particle Simulation"
        self.resolution = 50
        self.composeField()
    
    def composeField(self):
        self.vecfield = Field(ps.sysvals.getDims(), self.resolution)
        self.updateField()

    # TODO: Particles go out of bound, field wraps but particles do not.
    # QUESTION: Rate of diffusion of the field as rate of causality? light speed?
    def updateField(self):
        for i, f in enumerate(self.vecfield._field):
            if f:
                self.vecfield._field[i] = (0, 0)
                neighs = self.vecfield.getNeighborIndices(i)
                for n in neighs:
                    fn = self.vecfield._field[n]
                    if fn:
                        self.vecfield._field[n] = (self.vecfield._field[n][0] + f[0]/8, self.vecfield._field[n][1] + 1)
                    else:
                        self.vecfield._field[n] = (f[0]/8, 2)

        for e in self.entities:
            i, p = self.vecfield.valueAt(e.position)
            if i:
                val = 0
                if e.type == EParticleType.BLUE:
                    val = 1
                else:
                    val = -1
                if p:
                    self.vecfield._field[i] = (self.vecfield._field[i][0] + val, self.vecfield._field[i][1] + val)
                else:
                    self.vecfield._field[i] = (val, val)       

    def _handleInputEvents(self):
        super()._cursorEventCheck()
        super()._baseEventCheck()
        for e in self._events:
            if e.type == pg.MOUSEBUTTONDOWN:
                match(e.button):
                    case pg.BUTTON_LEFT:
                        mx, my = pg.mouse.get_pos()
                        self.clicked(mx, my, True, False)
                        continue
                    case pg.BUTTON_RIGHT:
                        mx, my = pg.mouse.get_pos()
                        self.clicked(mx, my, False, False)
                        continue
        self._events = []

    def click_at(self, dx, dy, ext):
        self.entities.append(Particle(pos=Vector2D(dx, dy), type = EParticleType.BLUE if ext else EParticleType.RED))

    # !Override ViewFrame! #
    def _inner_update(self):
        pcache = []
        dcache = []

        avgVel = 0
        maxVel = 0
        minVel = 0
        avgPosX = 0
        avgPosY = 0
        avgCount = 0
        self.updateField()
        for i, e in enumerate(self.entities):
            # Should always be a particle anyway.
            if not isinstance(e, Particle):
                continue

            # If a particle has been flagged to delete or is otherwise unactive
            if not e.active:
                dcache.append(e)
                continue

            # Statistics
            if e.velocity.magnitude() > maxVel:
                maxVel = e.velocity.magnitude()
            elif e.velocity.magnitude() < minVel:
                minVel = e.velocity.magnitude()
            avgPosX += e.x
            avgPosY += e.y
            avgCount += 1

            # Apply G force
            self.iterativeGravity(i, e)
            self.applyField(i, e)

            e.move()
            avgVel += e.velocity.magnitude()
        if avgCount == 0:
            avgCount = 1
        avgPosX = float(avgPosX / avgCount)
        avgPosY = float(avgPosY / avgCount)
        if self.debugmode:
            ps.renderer.drawCircle(Vector2D(avgPosX, avgPosY), 10, color=ps.sysvals.COLORS['green'])
            for j, f in enumerate(self.vecfield._field):
                if f:
                    ps.renderer.drawRectRGB(self.vecfield.getCoordsAt(j, True), 0, min(255, max((f[0] * 15)+128, 0)), 0, self.vecfield.resolution)
        deleted = 0
        for d in dcache:
            if d in self.entities:
                self.entities.remove(d)
                deleted += 1
        return (minVel, maxVel, avgVel, avgCount, avgPosX, avgPosY)

    def applyField(self, i: int, e: Particle):
        j, v = self.vecfield.get(vec=e.position)
        if j:
            maxV, maxI = -1, -1
            minV, minI = 999, 999
            valT = 0
            for n in self.vecfield.getNeighborIndices(j):
                c = self.vecfield._field[n][0]
                if c > maxV:
                    maxV = c
                    maxI = n
                if c < minV:
                    minI = n
                    minV = c
            if e.type == EParticleType.BLUE:
                coords = self.vecfield.getCoordsAt(maxI, True)
                valT = maxV
                dist = e.position - coords
            else:
                coords = self.vecfield.getCoordsAt(minI, True)
                valT = minV
                dist = e.position - coords

            dist = dist.normalize() * ps.sysvals.GRAV_CONST * math.sqrt(abs(valT))
            ps.renderer.drawCircle(coords, 10, 'yellow')
            e.velocity = e.velocity - dist

    def iterativeGravity(self, i, e):
        for p in self.entities[i+1:]:
            newps = e.gravity(p)
            e.collide(p)