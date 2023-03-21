from psim.inputhandler import InputEvent
from psim.math import Field, Vector2D
from psim.particle import EParticleType, Particle
from psim.simulation.simulation import Simulation
import pygame as pg
import psim as ps

class ParticleSimulation(Simulation):
    def __init__(self, numParticles):
        super().__init__()
        self.entities: list[Particle] = [Particle(type=EParticleType.BLUE) for _ in range(numParticles)]
        self.label = "Particle Simulation"
        self.resolution = 25
        self.composeField()
    
    def composeField(self):
        self.vecfield = Field(ps.sysvals.getDims(), self.resolution)
        self.updateField()

    # TODO: Particles go out of bound, field wraps but particles do not.
    # QUESTION: Rate of diffusion of the field as rate of causality? light speed?
    def updateField(self):
        for i, f in enumerate(self.vecfield._field):
            if f:
                if f[0] > 0:
                    self.vecfield._field[i] = None
                    neighs = self.vecfield.getNeighborIndices(i)
                    for n in neighs:
                        fn = self.vecfield._field[n]
                        if fn:
                            self.vecfield._field[n] = (self.vecfield._field[n][0] + f[0]/8, self.vecfield._field[n][1] + 1)
                        else:
                            self.vecfield._field[n] = (f[0]/8, 2)
                else:
                    self.vecfield._field[i] = None

        for e in self.entities:
            i, p = self.vecfield.valueAt(e.position)
            if i:
                if p:
                    self.vecfield._field[i] = (self.vecfield._field[i][0] + 1, self.vecfield._field[i][1] + 1)
                else:
                    self.vecfield._field[i] = (1,1)       

    def _handleInputEvents(self):
        super()._cursorEventCheck()
        super()._baseEventCheck()
        for e in self._events:
            match(e):
                case InputEvent.MOUSE_CLICK_LEFT:
                    mx, my = pg.mouse.get_pos()
                    self.clicked(mx, my, True, False)
                    continue
                case InputEvent.MOUSE_CLICK_RIGHT:
                    mx, my = pg.mouse.get_pos()
                    self.clicked(mx, my, False, False)
                    continue
        self._events = []

    def click_at(self, dx, dy, ext):
        self.entities.append(Particle(pos=Vector2D(dx, dy), type = EParticleType.BLUE if ext else EParticleType.RED))
        print(self.vecfield.get(vec=(dx, dy)))

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
            if e.velocity > maxVel:
                maxVel = e.velocity
            elif e.velocity < minVel:
                minVel = e.velocity
            avgPosX += e.x
            avgPosY += e.y
            avgCount += 1

            # Apply G force
            self.iterativeGravity(i, e)

            e.move()
            avgVel += e.velocity
        if avgCount == 0:
            avgCount = 1
        avgPosX = float(avgPosX / avgCount)
        avgPosY = float(avgPosY / avgCount)
        if self.debugmode:
            ps.renderer.drawCircle(Vector2D(avgPosX, avgPosY), 10, color=ps.sysvals.COLORS['green'])
            for j, f in enumerate(self.vecfield._field):
                if f:
                    ps.renderer.drawRectRGB(self.vecfield.getCoordsAt(j, True), 0, min(255, f[0]*15), 0, self.vecfield.resolution)
        deleted = 0
        for d in dcache:
            if d in self.entities:
                self.entities.remove(d)
                deleted += 1
        return (minVel, maxVel, avgVel, avgCount, avgPosX, avgPosY)

    def iterativeGravity(self, i, e):
        for p in self.entities[i+1:]:
            newps = e.gravity(p)
            e.collide(p)